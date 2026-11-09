import { readdir, readFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { SKILLS } from './skills.mjs';
const root = process.cwd();
async function walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (['.git', 'node_modules', '__pycache__', 'dist'].includes(entry.name)) continue;
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) await walk(path);
    else {
      const content = await readFile(path, 'utf8');
      if (/-----BEGIN (?:PRIVATE|RSA PRIVATE|EC PRIVATE) KEY-----/.test(content)) throw Error('Private key found: ' + entry.name);
      if (/C:\\Users\\|\/Users\/[A-Za-z]|\/home\/[a-z]|gh[pousr]_[A-Za-z0-9]{20,}/.test(content)) throw Error('Private path or credential found: ' + entry.name);
    }
  }
}
await walk(root);
for (const name of SKILLS) {
  const md = await readFile(join(root, 'skills', name, 'SKILL.md'), 'utf8');
  if (!new RegExp('^---\\nname: ' + name + '\\ndescription: .{40,}\\n', 'm').test(md.replace(/\r/g, ''))) throw Error('Bad frontmatter: ' + name);
}
console.log('Public source checks passed.');
