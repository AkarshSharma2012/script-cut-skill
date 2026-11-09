import { cp, mkdir, lstat, access, readFile, rename, rm } from 'node:fs/promises';
import { constants } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { randomUUID } from 'node:crypto';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

import { SKILLS } from './skills.mjs';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const opt = n => { const i = args.indexOf(n); if (i < 0) return undefined; const v = args[i + 1]; if (!v || v.startsWith('--')) throw Error(n + ' requires a value'); return v; };
const hosts = {
  claude: join(homedir(), '.claude', 'skills'),
  codex: join(homedir(), '.codex', 'skills'),
  agents: join(homedir(), '.agents', 'skills'),
  jcode: join(homedir(), '.jcode', 'skills'),
};

async function exists(p) { try { await access(p, constants.F_OK); return true; } catch { return false; } }

async function run() {
  const host = opt('--host'), targetArg = opt('--target');
  const dir = targetArg ? resolve(targetArg) : hosts[host];
  if (!dir) throw Error('Use --host claude|codex|agents|jcode or --target <skills-directory>. Add --replace to back up and replace installed copies.');
  if (dir === join(root, 'skills')) throw Error('Choose a skills directory outside this repository.');
  const replace = args.includes('--replace');
  const backupRoot = resolve(opt('--backup-dir') || join(homedir(), '.script-cut', 'backups'));

  // check everything before touching anything
  const present = [];
  for (const name of SKILLS) {
    const t = join(dir, name);
    if (!(await exists(t))) continue;
    if ((await lstat(t)).isSymbolicLink()) throw Error('Refusing to replace a symlink: ' + t);
    const md = await readFile(join(t, 'SKILL.md'), 'utf8').catch(() => '');
    if (!new RegExp('^name:\\s*' + name + '\\s*$', 'm').test(md)) throw Error('Existing folder is not the ' + name + ' skill; refusing to touch it: ' + t);
    present.push(name);
  }
  if (present.length && !replace) throw Error('Already installed: ' + present.join(', ') + '. Use --replace after reviewing the new version.');

  await mkdir(dir, { recursive: true });
  const batch = join(backupRoot, (host || 'custom') + '-' + randomUUID());
  const staged = [];
  try {
    for (const name of SKILLS) {
      const s = join(dir, '.script-cut-staging-' + name + '-' + randomUUID());
      await cp(join(root, 'skills', name), s, { recursive: true, errorOnExist: true, force: false });
      staged.push([name, s]);
    }
    if (present.length) await mkdir(batch, { recursive: true });
    for (const [name, s] of staged) {
      const t = join(dir, name);
      if (present.includes(name)) await rename(t, join(batch, name));
      await rename(s, t);
    }
  } catch (e) {
    for (const [, s] of staged) await rm(s, { recursive: true, force: true });
    throw e;
  }
  if (present.length) console.log('Previous skills backed up outside skill discovery: ' + batch);
  console.log([
    'Installed ' + SKILLS.length + ' skills into: ' + dir,
    'Restart the agent if its skill list is cached.',
    'Commands:',
    '  /script-find    find a script for your event and theme',
    '  /script-explain build-up, climax, conclusion, scenes, characters',
    '  /script-cut     cut a script to under 10 minutes at your pace',
    '  /script-block   blocking + how-to-say-it notes on every line',
    '  /script-intro   write intro options',
    '  /script-time    time it from word count or your stopwatch run',
    '  /script-judge   ballot-style review: can it break?',
    'No slash commands? Say "Use script-cut to cut <file> for DI".',
    'The cut tool needs Python 3 with: pip install pypdf python-docx',
    'No accounts, plugins, or paid services were installed.',
  ].join('\n'));
}
run().catch(e => { console.error(e.message); process.exitCode = 1; });
