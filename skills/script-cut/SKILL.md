---
name: script-cut
description: Cut a play, book, or screenplay into a competition-ready 10-minute speech and debate interp cutting (DI, HI, Duo, POI) with exact-source verification, timing at the student's pace, teaser + intro, and line-by-line blocking and delivery tags in the student's own voice. Use when the user says /script-cut or asks to cut a script for interp.
---

# /script-cut

Turn a full script into a cutting the student can perform under 10:00.

Usage: `/script-cut <script pdf/docx/txt> [event DI|HI|Duo|POI] [target time] [wpm or timed run] [notes]`

## First
1. Read `references/interp-guide.md` (rules, pace, what judges reward, user style, folders). Follow it exactly.
2. If the working folder has `SHARED_CONTEXT.md`, read it.
3. Need the user's own copy of the script (uploaded or on disk). If they only have a link, give a cutting plan, not the full text.

## Steps
1. **Extract:** `python scripts/build_cut.py extract <source.pdf> tmp/source.txt`. Read the whole thing.
2. **Plan before cutting** (show this briefly, then keep going unless the user wants to approve):
   - climax (pick first), teaser (first 30-60 sec), 8-12 beats, ending that echoes the opening
   - what's cut and why (summary, side plots, audience participation, extra characters)
   - for DI: monologue style, no popping unless asked
3. **Write `tmp/cut.json`** (format is in the docstring of `scripts/build_cut.py`):
   - `src` = exact author lines, in source order. Cut whole sentences or clean phrases only.
   - `intro` = new intro (45-100 words, ends with title + author).
   - `cue` = blocking commands. `tag` on every spoken line = how to say it.
   - Notes in the user's voice: lowercase, short, "ur", no jargon. Commands, not suggestions.
   - `backup_cuts` (5) + `never_cut`.
4. **Check:** `python scripts/build_cut.py check <source> tmp/cut.json --wpm <pace>`
   - `unverified_lines` must be empty. Fix the text to match the source, never the other way.
   - `possibly_out_of_order`: fix or confirm it's a PDF glitch.
   - Trim or add source lines until `talking_minutes` + ~1 min lands at 9:00-9:30.
5. **Clarity pass:** read it as a judge who never saw the play. Every new person, place, or time jump needs one source line that explains it. Fix fragments.
6. **Build:** `python scripts/build_cut.py build <source> tmp/cut.json "<folder>\<Script> <EVENT> cut.docx" --wpm <pace>`
7. **File it** per the guide: `orginal scripts\`, `cutted scripts\<Script>\` + `precutted\`, copy to Downloads. Never overwrite the user's Google Docs.
8. **Reply** (under ~12 lines): file path, spoken words, estimated time (say it's an estimate), the arc in one line, what was cut, and "time one full run and tell me."

## Edits later
Keep `tmp/cut.json`. For changes ("less popping", "clearer notes", "make it the best"), edit the JSON, re-run check + build, save over the same file, keep a backup copy.
