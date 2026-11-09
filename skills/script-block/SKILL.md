---
name: script-block
description: Add or rewrite blocking and delivery notes on a speech and debate interp cutting, giving every spoken line a clear how-to-say-it tag and every move a command, written the way the student talks. Use when the user says /script-block or asks for blocking, voice notes, or clearer instructions.
---

# /script-block

Usage: `/script-block <cut file> [notes like "less popping" or "make them clearer"]`

1. Read `../script-cut/references/interp-guide.md`, especially the user style section. Read `SHARED_CONTEXT.md` if present.
2. Never change the spoken words. Only add or rewrite `[brackets]`.
3. **Cue lines** (own line, before the action): commands. Where to stand/sit, what to mime, how many secs to hold, where to look. Plain directions ("ur back left").
4. **Tag on every spoken line** (in front of it): whose voice (kid/teen/adult/ur real voice), pitch, volume, speed, exact word to pause/stutter/crack/hit, face or body move.
5. Rules:
   - Mime everything, no props. Floor work okay but flag it once for the coach.
   - DI = mostly monologue: quoted characters in the narrator's own voice unless the user wants pops.
   - Stutters and pauses never add extra words.
   - Give the climax the most silence and stillness. Give early comedy clear "wait for the laugh" notes.
   - Repeat a gesture from the opening at the end (echo) when it fits.
6. Rebuild with `../script-cut/scripts/build_cut.py build` if a `cut.json` exists, else edit the .docx directly. Save over the same file, copy to Downloads.
