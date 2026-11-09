---
name: script-time
description: Time a speech and debate interp cutting from word count and the student's pace, or from a real timed run, and say exactly what to cut or add to land at 9:00-9:30 under the 10:00 limit. Use when the user says /script-time or gives a run time.
---

# /script-time

Usage: `/script-time <cut file> [my run was 9:48] [wpm]`

1. Read `../script-cut/references/interp-guide.md` (pace rules). Read `SHARED_CONTEXT.md` if present.
2. Count spoken words only (script lines + intro, not [brackets] or headers). If the cut has a `tmp/cut.json`, run `python ../script-cut/scripts/build_cut.py check <source> tmp/cut.json --wpm <pace>`.
3. If the user gave a real run time: new wpm = spoken words / run minutes. Save that pace to `SHARED_CONTEXT.md` as their solo pace.
4. Reply:
   - spoken words, pace used, talking time, estimated total with pauses
   - **over 9:30:** list exact lines to cut (use the doc's "IF UR OVER TIME" list first), with seconds saved each, until it fits
   - **under 8:45:** suggest source lines to add back that strengthen the climax or a live scene
   - remind: 10:00 + 30s grace, over grace = can't take 1st
5. Only edit the file if the user says to. Then re-run check + build and save over it.
