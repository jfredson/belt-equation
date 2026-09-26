#!/usr/bin/env python3
"""Checks on the one-command publish (website step 26, 2026-09-25).

Plain Python, standard library only, no dependencies beyond what the site build already needs
(Node and the site's packages in site/node_modules):

    python3 scripts/test_publish.py

The check that matters: `python3 scripts/publish.py` without --push must leave a working tree
in exactly the state the manual route leaves it in, which is `python3 scripts/export.py` and
then `npm run build` in site/. So the test copies the working tree twice into scratch folders,
makes each a git repository with one commit, runs the publish script in one and the manual
route in the other, and compares:

- every file the export writes (site/src/data/*.json and site/public/tree.svg), byte for byte;
- every file of the built site in site/dist/, byte for byte, except the decorative stars behind
  each page, which the site scatters at random on every build (same_page, below);
- every file git can see, so the publish script changed nothing else, with one allowance: a new
  dated copy of the tree picture under docs/visual/, which the script keeps when the picture has
  changed since the newest copy and which the manual route does not make.

It also checks that the publish script made no commit, since it was not given --push, and that
--dry-run writes nothing at all. The story refresh is turned off (--no-story) so the test never
calls TimeAssembler and runs the same with or without the key.

Slow on purpose: two exports, two site builds, one dry run and one reading of the committed
tree, about five minutes on the Mac.
"""

from __future__ import annotations

import filecmp
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import publish  # noqa: E402

ROOT = HERE.parent
GIT = ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false"]


def scratch_repo(where: Path) -> Path:
    """A copy of the working tree as a git repository of its own with one commit.

    The commit's dates are fixed, so two copies made a moment apart get the same commit id: the
    export writes the id into tree.json and the site prints it, and a different id would be a
    difference between the copies rather than between the two routes."""
    repo = where / "repo"
    publish.copy_working_tree(ROOT, repo)
    fixed = dict(os.environ, GIT_AUTHOR_DATE="2026-09-25T12:00:00Z", GIT_COMMITTER_DATE="2026-09-25T12:00:00Z")
    subprocess.run([*GIT, "init", "-q", "-b", "main"], cwd=repo, check=True)
    subprocess.run([*GIT, "add", "-A"], cwd=repo, check=True)
    subprocess.run([*GIT, "commit", "-q", "-m", "scratch copy"], cwd=repo, check=True, env=fixed)
    return repo


def files_under(folder: Path) -> dict[str, Path]:
    return {str(p.relative_to(folder)): p for p in sorted(folder.rglob("*")) if p.is_file()}


STARFIELD = re.compile(r'(<div class="starfield"[^>]*>).*?(</div>)', re.S)


def same_page(a: Path, b: Path) -> bool:
    """Byte for byte, except the stars behind every page. site/src/components/Starfield.astro
    scatters them with Math.random() at build time, so no two builds of the site are identical,
    manual or not; the pages are compared with the stars taken out."""
    if a.suffix != ".html":
        return filecmp.cmp(a, b, shallow=False)
    strip = lambda p: STARFIELD.sub(r"\1\2", p.read_text())  # noqa: E731
    return strip(a) == strip(b)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, TZ=publish.TZ)
    return subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


@unittest.skipUnless((ROOT / "site" / "node_modules").is_dir(),
                     "the site's packages are not installed (cd site && npm ci)")
class PublishMatchesTheManualRoute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        base = Path(cls._tmp.name)
        cls.published = scratch_repo(base / "published")
        cls.manual = scratch_repo(base / "manual")
        cls.head_before = cls.head(cls.published)

        cls.publish_run = run([sys.executable, "scripts/publish.py", "--no-story"], cls.published)
        cls.export_run = run([sys.executable, "scripts/export.py"], cls.manual)
        cls.build_run = run(["npm", "run", "build"], cls.manual / "site")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    @staticmethod
    def head(repo: Path) -> str:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                              text=True, stdout=subprocess.PIPE).stdout.strip()

    def assertSameFiles(self, a: Path, b: Path, what: str, same=filecmp.cmp):
        fa, fb = files_under(a), files_under(b)
        self.assertTrue(fa, f"{what}: nothing was generated")
        self.assertEqual(sorted(fa), sorted(fb), f"{what}: the two routes wrote different files")
        different = [rel for rel in fa if not same(fa[rel], fb[rel])]
        self.assertEqual(different, [], f"{what}: these files differ between the two routes")

    def test_both_routes_ran(self):
        self.assertEqual(self.publish_run.returncode, 0, self.publish_run.stdout)
        self.assertEqual(self.export_run.returncode, 0, self.export_run.stdout)
        self.assertEqual(self.build_run.returncode, 0, self.build_run.stdout)

    def test_the_site_data_is_the_same(self):
        self.assertSameFiles(self.published / "site" / "src" / "data",
                             self.manual / "site" / "src" / "data", "site/src/data")
        self.assertTrue(filecmp.cmp(self.published / "site" / "public" / "tree.svg",
                                    self.manual / "site" / "public" / "tree.svg", shallow=False),
                        "site/public/tree.svg differs between the two routes")

    def test_the_built_site_is_the_same(self):
        self.assertSameFiles(self.published / "site" / "dist", self.manual / "site" / "dist", "site/dist",
                             same=same_page)

    def test_nothing_else_changed(self):
        changed = publish.differences(publish.visible_files(self.manual), publish.visible_files(self.published))
        allowed = [line for line in changed if line.startswith("?? docs/visual/") and line.endswith("-tree.svg")]
        self.assertLessEqual(len(allowed), 1)
        self.assertEqual([line for line in changed if line not in allowed], [],
                         "publish.py changed files the manual route leaves alone")

    def test_no_commit_without_push(self):
        self.assertEqual(self.head(self.published), self.head_before, "publish.py committed without --push")
        self.assertIn("Stopped before committing", self.publish_run.stdout)

    def test_the_summary_shows_the_headline(self):
        self.assertIn("the headline, as last committed", self.publish_run.stdout)
        self.assertIn("by 2071", self.publish_run.stdout)


@unittest.skipUnless((ROOT / "site" / "node_modules").is_dir(),
                     "the site's packages are not installed (cd site && npm ci)")
class DryRunWritesNothing(unittest.TestCase):

    def test_dry_run_leaves_the_tree_alone(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = scratch_repo(Path(tmp))
            before = {rel: p.read_bytes() for rel, p in files_under(repo).items() if "/.git/" not in f"/{rel}"}
            result = run([sys.executable, "scripts/publish.py", "--dry-run", "--no-story", "--push"], repo)
            self.assertEqual(result.returncode, 0, result.stdout)
            after = {rel: p.read_bytes() for rel, p in files_under(repo).items() if "/.git/" not in f"/{rel}"}
            self.assertEqual(sorted(before), sorted(after), "--dry-run added or removed files")
            self.assertEqual([r for r in before if before[r] != after[r]], [], "--dry-run changed files")
            self.assertIn("nothing was written, committed or pushed", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
