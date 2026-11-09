# Install Script Cut

Read the repository before running scripts. Use a normal user shell, not administrator mode. Node 22+ is needed only for the installer. Nothing is downloaded by the installer.

```sh
git clone https://github.com/AkarshSharma2012/script-cut-skill.git
cd script-cut-skill
node scripts/install.mjs --host claude
```

Use `--host codex`, `--host jcode`, `--host agents`, or `--target <your agent's skills folder>` instead when that fits. Don't install into more than one skills folder for the same agent.

All seven skills install together: `script-cut`, `script-explain`, `script-find`, `script-time`, `script-block`, `script-judge`, `script-intro`. They share the guide and checker inside `script-cut`, so keep them in the same folder.

Existing copies are never overwritten by default. To update after reviewing changes, add `--replace`. The old copies are moved to a timestamped backup under `~/.script-cut/backups` first, outside skill discovery. Folders with the same name that aren't these skills, and symlinks, are refused.

## Python for the cut checker

```sh
pip install pypdf python-docx
```

Without these, the skills still work as instructions, but can't auto-verify lines against the source or build the .docx.

## Without Node

Copy every folder inside `skills/` into your agent's skills folder with normal file tools. If your agent can't install skills, ask it to read `skills/script-cut/SKILL.md` for the task.

For Claude Chat/Cowork, zip each skill folder so the archive root is `<skill-name>/SKILL.md`, and upload them through the skills settings. Include `script-cut` since the others point to its guide.

## First use

Try `/script-explain <your script>` or `/script-cut <your script> DI`. The first time you cut, the agent asks where you keep scripts (or uses an obvious speech and debate folder) and what your pace is. If you don't know your pace, it uses 149 words per minute until you time a real run with `/script-time`.

## Updating and removing

Pull the repo, review changes, then rerun the installer with `--replace`. To uninstall, delete the seven `script-*` folders from your skills folder. No hooks, services, scheduled jobs, accounts, or global settings were changed.
