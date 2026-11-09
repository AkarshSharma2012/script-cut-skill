# Security

- The installer only copies the `skills/` folders into the skills directory you choose. It never runs downloaded code, changes global settings, or touches accounts.
- Existing skills are not overwritten without `--replace`, and replaced copies are backed up first. Symlinks and unrelated folders with the same name are refused.
- The skills tell the agent never to contact anyone (email, chat, text) and never to edit the user's original scripts or documents.
- No telemetry, analytics, or network calls are made by the installer or the checker.

Report problems by opening an issue. Don't include private scripts or personal information.
