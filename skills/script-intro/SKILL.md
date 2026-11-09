---
name: script-intro
description: Write or rewrite the teaser and intro for a speech and debate interp cutting (why it matters, then title and author), sized to the time budget and the student's voice. Use when the user says /script-intro or asks for an intro.
---

# /script-intro

Usage: `/script-intro <cut file or script> [theme/argument] [word limit]`

1. Read `../script-cut/references/interp-guide.md`. Read `SHARED_CONTEXT.md` if present.
2. Find the cut's theme and the teaser's last line (the intro follows it).
3. Write 2-3 options, 45-100 words each:
   - open with a universal idea or real-world issue the piece speaks to
   - one line on what happens (no spoilers of the climax)
   - end with: `<Title>, by <Author>.`
   - sounds like a smart high schooler talking, not an essay
4. Give each option a word count and seconds at the user's pace.
5. Only put it in the file if the user picks one. Then update `cut.json`, re-run check + build, save over the same file.
