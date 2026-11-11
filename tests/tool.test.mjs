import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const tool = resolve('skills/script-cut/scripts/build_cut.py');
const py = process.platform === 'win32' ? 'python' : 'python3';
const has = spawnSync(py, ['-c', 'import docx'], { encoding: 'utf8' }).status === 0;

// public domain source (Shakespeare)
const SOURCE = `HAMLET. To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die: to sleep;
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to.`;

async function setup(segments) {
  const d = await mkdtemp(join(tmpdir(), 'script-cut-tool-'));
  await writeFile(join(d, 'src.txt'), SOURCE);
  await writeFile(join(d, 'cut.json'), JSON.stringify({ title: 'Hamlet', author: 'William Shakespeare', segments, backup_cuts: ["1. 'To die: to sleep;' (~2 sec)"], never_cut: 'the question' }));
  return d;
}
const call = (d, ...a) => spawnSync(py, [tool, ...a.map(x => x.replace('$', d))], { encoding: 'utf8' });

test('check passes exact excerpts and counts words', { skip: !has && 'python-docx not installed' }, async () => {
  const d = await setup([
    { kind: 'cue', text: '[stand still]' },
    { kind: 'src', text: 'To be, or not to be, that is the question:', tag: '[slow]' },
    { kind: 'intro', text: 'Doubt. Hamlet, by William Shakespeare.', tag: '[own voice]' },
    { kind: 'src', text: 'To die: to sleep;', tag: '[quiet]' },
  ]);
  const r = call(d, 'check', '$/src.txt', '$/cut.json', '--wpm', '120');
  assert.equal(r.status, 0, r.stderr);
  const j = JSON.parse(r.stdout);
  assert.equal(j.unverified_lines.length, 0);
  assert.equal(j.intro_words, 5);
  assert.equal(j.spoken_words, 19);
});

test('check flags rewritten lines and out-of-order lines', { skip: !has && 'python-docx not installed' }, async () => {
  const d = await setup([
    { kind: 'src', text: 'The heart-ache and the thousand natural shocks That flesh is heir to.', tag: '[x]' },
    { kind: 'src', text: 'Whether tis nobler in the mind to suffer The slings and arrows', tag: '[x]' },
    { kind: 'src', text: 'To exist or not exist, that is my big question today', tag: '[x]' },
  ]);
  const r = call(d, 'check', '$/src.txt', '$/cut.json');
  assert.equal(r.status, 2);
  const j = JSON.parse(r.stdout);
  assert.equal(j.unverified_lines.length, 1);
  assert.equal(j.possibly_out_of_order.length, 1);
});

test('build writes a docx with tags and backup cuts', { skip: !has && 'python-docx not installed' }, async () => {
  const d = await setup([{ kind: 'src', text: 'To be, or not to be,', tag: '[slow]' }]);
  const r = call(d, 'build', '$/src.txt', '$/cut.json', '$/out.docx');
  assert.equal(r.status, 0, r.stderr);
  const txt = spawnSync(py, ['-c', `import docx;print('\\n'.join(p.text for p in docx.Document(r'${join(d, 'out.docx')}').paragraphs))`], { encoding: 'utf8' }).stdout;
  assert.ok(txt.includes('slow'));
  assert.ok(txt.includes('To be, or not to be,'));
  assert.ok(!txt.includes('[slow]'), 'brackets are stripped in the new layout');
  assert.ok(txt.includes('IF UR OVER TIME'));
});
