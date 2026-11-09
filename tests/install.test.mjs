import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, readFile, writeFile, readdir, mkdir } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { SKILLS } from '../scripts/skills.mjs';
const installer = resolve('scripts/install.mjs');
const run = a => execFileSync(process.execPath, [installer, ...a], { encoding: 'utf8', stdio: 'pipe' });

test('installs all skills with references and tool, refuses clobber, backs up on replace', async () => {
  const root = await mkdtemp(join(tmpdir(), 'script-cut-install-')), dir = join(root, 'skills');
  const out = run(['--target', dir]);
  assert.ok(out.includes('/script-cut'));
  for (const name of SKILLS) assert.match(await readFile(join(dir, name, 'SKILL.md'), 'utf8'), new RegExp('^name: ' + name + '$', 'm'));
  assert.ok((await readFile(join(dir, 'script-cut', 'references', 'interp-guide.md'), 'utf8')).includes('Cut, don\'t rewrite'));
  assert.ok((await readFile(join(dir, 'script-cut', 'scripts', 'build_cut.py'), 'utf8')).includes('def check'));
  await writeFile(join(dir, 'script-cut', 'my-note.txt'), 'preserve');
  assert.throws(() => run(['--target', dir]));
  const replaced = run(['--target', dir, '--replace', '--backup-dir', join(root, 'backups')]);
  const backup = replaced.split('\n').find(x => x.startsWith('Previous skills backed up')).split(': ').slice(1).join(': ').trim();
  assert.equal(await readFile(join(backup, 'script-cut', 'my-note.txt'), 'utf8'), 'preserve');
  assert.ok(!(await readdir(join(dir, 'script-cut'))).includes('my-note.txt'));
  assert.equal((await readdir(dir)).filter(x => x.startsWith('.script-cut-staging')).length, 0);
});

test('refuses to replace a folder that is not this skill', async () => {
  const root = await mkdtemp(join(tmpdir(), 'script-cut-foreign-')), dir = join(root, 'skills');
  await mkdir(join(dir, 'script-time'), { recursive: true });
  await writeFile(join(dir, 'script-time', 'SKILL.md'), '---\nname: something-else\n---\n');
  assert.throws(() => run(['--target', dir, '--replace']));
  assert.equal(await readFile(join(dir, 'script-time', 'SKILL.md'), 'utf8'), '---\nname: something-else\n---\n');
});

test('rejects missing target', () => { assert.throws(() => run(['--target'])); assert.throws(() => run([])); });
