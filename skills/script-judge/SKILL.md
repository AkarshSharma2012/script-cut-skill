---
name: script-judge
description: Judge a speech and debate interp cutting like a tournament ballot, checking it is blockable, understandable, under time, follows DI/HI/Duo rules, and has what it takes to break and bid, then list the top fixes. Use when the user says /script-judge or asks if a script is good enough to break or get a bid.
---

# /script-judge

Usage: `/script-judge <cut file> [event]`

1. Read `../script-cut/references/interp-guide.md`. Read `SHARED_CONTEXT.md` if present. If a source and `cut.json` exist, run the check script.
2. Read the cut as a judge who never saw the source.
3. Reply with a short ballot:
   - **Blockable?** yes/no + any spot that can't be mimed or breaks a rule
   - **Understandable?** list any "who/where/when?" moment a judge would get lost on
   - **Rules:** time estimate, one source, cut-only (no added words), no props, event fit
   - **Strengths** (3 bullets)
   - **Risks** (up to 5, honest)
   - **Can it break/bid?** "Yes if..." Never promise a bid. Say what the performance must nail.
   - **Top 3 fixes** ranked by impact
4. Offer to apply the fixes. Don't edit unless the user says to (or says "make it the best"). Then apply using `/script-cut` edit steps.
