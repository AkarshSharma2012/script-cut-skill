# Launch kit

Ready-to-post drafts and the plan for where to post them. Based on what actually works for open source launches (sources at the bottom).

## Rules that matter most
1. **Lead with the problem, not "please star".** Reddit and HN punish self-promo. Tell the story: "I'm a high schooler, cutting scripts took my whole weekend, so I built this."
2. **Launch everything in one 48-hour window.** GitHub Trending ranks by stars gained in a short window, so spreading posts over weeks wastes them.
3. **Best time:** Tuesday to Thursday, 8-10am ET.
4. **Reply to every comment within an hour** on launch day.
5. **Read each subreddit's rules first.** Some ban self-promo or only allow it on certain days. Getting removed hurts more than not posting.
6. **Never buy stars.** GitHub removes them and it violates their rules.
7. **After launch, keep shipping.** Post updates when you add features ("now supports Duo", "now supports NCFCA rules").

## Day 0 (before launch)
- [ ] Repo public, CI green, demo image showing.
- [ ] Add topics (already done by setup): `claude-code`, `agent-skills`, `speech-and-debate`, `forensics`, `education`, ...
- [ ] Open 3-5 "good first issue" issues (already done by setup).
- [ ] Ask teammates and friends who'd actually use it to try it and star if useful (real users only).
- [ ] Submit to skill directories (no launch timing needed, do these first):
  - [awesomeskills.dev/submit](https://www.awesomeskills.dev/en/submit) (paste repo URL)
  - [skillsdirectory.com](https://www.skillsdirectory.com/) (Submit a skill)
  - [claudeskills.info](https://claudeskills.info/agent-skills/directory/) (submission form)
  - PRs to awesome lists: [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills), [BehiSecc/awesome-claude-skills](https://github.com/BehiSecc/awesome-claude-skills), [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills), [heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills)
  - Full list of places with steps: [vawe-hq/awesome-agent-skills-directories](https://github.com/vawe-hq/awesome-agent-skills-directories)

## Day 1 (launch, Tue-Thu morning ET)
- [ ] Hacker News: Show HN post (draft below)
- [ ] Reddit: r/ClaudeAI, r/ClaudeCode, r/SideProject, r/coolgithubprojects (drafts below)
- [ ] X thread (draft below)
- [ ] Instagram/TikTok reel (script below)
- [ ] Speech and debate Discord servers and team group chats (draft below)

## Day 2-7
- [ ] dev.to "How I built it" post (draft below)
- [ ] r/Debate (check rules first), speech coaches you personally know
- [ ] Reply, fix the bugs people find, post a "thanks + what changed" update

---

## Show HN

**Title:** Show HN: Script Cut – AI agent skills that cut plays into 10-minute speech and debate pieces

**Text:**
I'm a high school student in speech and debate. Every season the worst part is cutting a script: you take a 60-page play and turn it into a 10-minute performance, count words by hand, run it, go over time, and repeat.

I built 7 agent skills (Claude Code, Codex, any agent that reads SKILL.md) that do it: find a script, cut it to time at your own speaking pace, and add blocking and delivery notes to every line.

The part I care about most: competition rules say you can cut but never add words. So there's a small Python checker that verifies every spoken line against the source text and flags anything rewritten or out of order. LLMs love to "improve" lines, and that would get a student disqualified.

Repo: https://github.com/AkarshSharma2012/script-cut-skill

Would love feedback, especially from anyone who did forensics.

---

## Reddit: r/ClaudeAI / r/ClaudeCode

**Title:** I made Claude skills that cut plays into 10-minute speech & debate pieces (and verify it never changes a word)

**Body:**
I'm in high school speech and debate (Dramatic Interp). Cutting a script down to 10 minutes used to take me a whole weekend.

So I turned my workflow into 7 skills: `/script-find`, `/script-explain`, `/script-cut`, `/script-block`, `/script-time`, `/script-judge`, `/script-intro`.

The tricky part was that Claude kept "improving" lines, and in competition you can only cut, never add words. I fixed that with a checker script that compares every spoken line to the original PDF and flags anything that doesn't match.

It also writes blocking notes in plain language ("stand up. stare at an invisible dad for 3 secs") and a how-to-say-it tag on every line.

[screenshot of demo.png]

Repo + install: https://github.com/AkarshSharma2012/script-cut-skill

What I learned building it: give the model a verifier instead of more instructions. Happy to answer questions.

---

## Reddit: r/SideProject / r/coolgithubprojects

**Title:** Built a tool that turns a 60-page play into a 10-minute speech & debate performance

**Body:**
High schooler here. Speech and debate kids spend hours cutting scripts down to 10 minutes. I built agent skills that do it at your own pace, add blocking and voice notes to every line, and check that no words were changed (you get DQ'd for adding words).

[screenshot]

https://github.com/AkarshSharma2012/script-cut-skill

Free, open source, MIT. Feedback welcome.

---

## X thread

1/ I'm a high school speech & debate kid. Cutting a script to 10 minutes takes forever.

So I built 7 AI agent skills that do it. 🧵

2/ `/script-cut my-play.pdf DI`

You get a doc sized to your speaking pace, with blocking + a how-to-say-it note on every line. [demo.png]

3/ The hard part: competition rules say you can cut, never add words. LLMs love to "fix" lines.

So a checker verifies every line against the original and flags anything changed.

4/ Other commands:
/script-find – find a script
/script-explain – climax, scenes, characters
/script-time – what to cut if you're over
/script-judge – ballot-style feedback

5/ Works in Claude Code, Codex, and any agent that reads SKILL.md. Free + open source.

https://github.com/AkarshSharma2012/script-cut-skill

Tag accounts: @AnthropicAI @claudeai (only once, in the last tweet)

---

## Instagram / TikTok reel (30-45 sec)

- 0-3s (hook, text on screen): "POV: you have to cut a 60 page play by Friday"
- 3-8s: scroll through a giant PDF, stressed
- 8-15s: type `/script-cut my-play.pdf DI` and hit enter
- 15-25s: scroll the finished doc, zoom on the blue notes ("[voice cracks on 'love']")
- 25-35s: perform 2 lines following the notes
- 35-45s: "free, link in bio" + repo name on screen

Caption: built this for my speech and debate team. free + open source. #speechanddebate #forensics #interp #DI #theatrekid #ai #claudeai

Hashtags speech kids actually follow: #speechanddebate #forensics #nsda #interp #dramaticinterp #duointerp #theatre

---

## Team Discord / group chat

hey! i made a thing that cuts scripts for interp. you give it the pdf and it cuts it to under 10 min at your pace with blocking notes on every line. free. lmk if it helps or if it breaks lol
https://github.com/AkarshSharma2012/script-cut-skill

---

## dev.to: "How I built it"

**Title:** I built AI skills that cut plays for speech and debate (and how I stopped the AI from changing words)

Outline:
1. The problem (cutting scripts, the "no added words" rule)
2. First try: just prompting. It kept rewriting lines.
3. The fix: a verifier. Normalize text, find each line in the source, flag low matches and out-of-order lines.
4. Making notes useful: commands, not suggestions, written the way students talk
5. Packaging as portable skills with a safe installer
6. What's next (more leagues, Duo support)
Link the repo at the top and bottom.

---

## Sources
- Lead with the problem, Reddit converts best when it's genuine, read sub rules: [Infrasity](https://www.infrasity.com/blog/how-to-get-github-stars), [Gingiris](https://gingiris.github.io/growth-tools/blog/2026/04/14/github-stars-growth-guide/)
- Coordinated 48-hour window, reply within an hour: [upvote.club](https://upvote.club/blog/how-to-get-github-stars)
- Show HN Tue-Thu 8-10am ET, concentrate launch on one day: [RepoClip](https://repoclip.io/blog/how-to-get-more-stars-on-github)
- One primary channel per push, fast replies: [dev.to](https://dev.to/iris1031/github-star-growth-8-compounding-plays-for-2026-4dk9)
- Where to list agent skills: [awesome-agent-skills-directories](https://github.com/vawe-hq/awesome-agent-skills-directories)
