#!/bin/bash
# The daily launch-day check for the Missions page (scripts/missions_watch.py; tracker pattern rule
# 4.20, ruled by John 2026-10-21). launchd runs this once a day from a copy in
# ~/Library/Application Support/belt-missions-watch/. It runs the scripts as they are on the
# repository's main branch, so the job follows whatever John has merged and never a working branch.
# It edits nothing and publishes nothing: at most it files a TimeAssembler task for John.
set -euo pipefail
HOME_DIR="$HOME/Library/Application Support/belt-missions-watch"
REPO="$HOME/Code/belt-equation"
RUN="$HOME_DIR/run"
mkdir -p "$RUN"
git -C "$REPO" fetch -q origin main
for f in missions_watch.py missions.py; do
  if ! git -C "$REPO" show "origin/main:scripts/$f" > "$RUN/$f" 2>/dev/null; then
    echo "$(date +%F): scripts/$f is not on main yet; nothing to check."
    exit 0
  fi
done
exec "$HOME_DIR/venv/bin/python" "$RUN/missions_watch.py" --daily
