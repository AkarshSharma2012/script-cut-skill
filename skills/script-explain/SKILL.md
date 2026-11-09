---
name: script-explain
description: Explain a script or cutting for speech and debate interp, giving the summary, build-up, climax, conclusion, scene list, characters, and how many popping scenes. Use when the user says /script-explain or asks what happens in a script, what the scenes are, or what the climax is.
---

# /script-explain

Usage: `/script-explain <script or cut file> [full|cut]`

1. Read `../script-cut/references/interp-guide.md` for user style. Read `SHARED_CONTEXT.md` if present.
2. Read the whole file. For a PDF: `python ../script-cut/scripts/build_cut.py extract <pdf> tmp/source.txt`.
3. Reply in this shape, in plain casual words, no long paragraphs:
   - **What it is:** title, author, format (monologue / multi-character / screenplay / novel), original length, one-line premise.
   - **Build-up:** 3-6 bullets.
   - **Climax:** 1-3 bullets. Name the exact moment.
   - **Conclusion:** 2-4 bullets + the message in one line.
   - **Scenes:** numbered list, one line each, mark laughs and the climax.
   - **Characters:** who the performer plays, plus who is only listened to or mentioned.
   - **Popping:** how many scenes have real back-and-forth between characters vs. quick quotes.
   - **Interp fit (one line):** good for DI / HI / Duo / POI? Monologue or needs heavy cutting?
4. Flag content (suicide, abuse, language) in one line if present. Spoilers are fine, this is for prep.
5. Never quote long chunks of copyrighted text. Summarize.
