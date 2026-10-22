# The daily launch-day check

Ruled by John on 2026-10-21 (tracker pattern rule 4.20; docs/proposal-missions-to-watch-2026-10-20.md,
decision 11): a small daily job that checks only the next seven days' milestones on the Missions page,
paid from the monthly API credits, which proposes a post or a date change and never publishes on its own.

## What it does

Every morning at 07:40 Pacific, `missions-watch.sh` fetches the repository's main branch and runs
`scripts/missions_watch.py --daily` as it stands on main. The script reads `data/missions.toml` from
main and looks for planned milestones dated to a day or a month between three days ago and seven days
ahead. On most days there are none, and it stops without calling the API. When there are, it makes one
call to the Claude API with web search, asking what happened, and if anything happened, moved or failed
it files one task in the Belt Equation project in TimeAssembler for John to approve. It edits no file,
commits nothing and posts nothing.

- Key: the `weekly-readings` workspace key, `~/.config/sentient-horizons/anthropic-weekly-readings.env`
  (timeassembler/docs/session-routing.md). Never printed.
- Cost log: `~/Library/Logs/belt-missions-watch.csv`, one line per run that called the API, with the
  vendor "Anthropic credits". The spending record (docs/spending-record.md) holds the estimate.
- Output: `~/Library/Logs/belt-missions-watch.out.log` and `.err.log`.

## Install, and switch off

Installed on John's Mac on 2026-10-21, then switched off the same evening before a restart of the Mac, at the master session's request. It stays off until John says to switch it on. To install it:

    mkdir -p ~/Library/Application\ Support/belt-missions-watch
    python3 -m venv ~/Library/Application\ Support/belt-missions-watch/venv
    ~/Library/Application\ Support/belt-missions-watch/venv/bin/pip install anthropic
    cp scripts/launchd/missions-watch.sh ~/Library/Application\ Support/belt-missions-watch/
    cp scripts/launchd/com.sentienthorizons.belt-missions-watch.plist ~/Library/LaunchAgents/
    launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sentienthorizons.belt-missions-watch.plist

To switch it off:

    launchctl bootout gui/$(id -u)/com.sentienthorizons.belt-missions-watch

Until the Missions page is merged to main, the job finds no missions file there and stops at once.
