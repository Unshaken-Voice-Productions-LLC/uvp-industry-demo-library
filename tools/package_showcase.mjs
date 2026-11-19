/** Export only the reviewed gallery, demo distributions and legal notices. */
import {readFileSync, writeFileSync, mkdirSync, rmSync, lstatSync, realpathSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const text = file => readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
function plainFile(file) {
  const info = lstatSync(file);
  if (!info.isFile() || info.isSymbolicLink() || realpathSync(file) !== path.resolve(file)) throw new Error(`Expected a regular source file: ${file}`);
  return file;
}

export function packageShowcase(root = ROOT) {
  root = realpathSync(root);
  const catalog = path.join(root, '07_PORTFOLIO_INDEX');
  const sourceRoot = path.join(root, '03_RECONSTRUCTED_SITES');
  const out = path.join(root, 'showcase');
  const items = JSON.parse(text(plainFile(path.join(catalog, 'portfolio.json'))));
  if (!Array.isArray(items) || items.length !== 14) throw new Error('Expected the reviewed 14-demo catalog');
  let index = text(plainFile(path.join(catalog, 'index.html')));
  const ids = new Set();
  const exports = [];
  for (const item of items) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(item.id) || ids.has(item.id)) throw new Error('Invalid or duplicate demo identity');
    ids.add(item.id);
    const entry = path.resolve(catalog, item.demoPath);
    if (!entry.startsWith(sourceRoot + path.sep) || path.basename(entry) !== 'index.html' || path.basename(path.dirname(entry)) !== 'dist') throw new Error('Demo source escapes its distribution boundary');
    const source = path.dirname(entry);
    if (lstatSync(source).isSymbolicLink()) throw new Error('Distribution directories must not be symlinks');
    const href = `href="${item.demoPath}"`;
    if (index.split(href).length !== 2) throw new Error(`Catalog link is missing or duplicated: ${item.id}`);
    index = index.replace(href, `href="demos/${item.id}/index.html"`);
    for (const name of ['index.html', 'styles.css', 'script.js']) {
      const file = plainFile(path.join(source, name));
      let bytes = readFileSync(file);
      if (name === 'index.html') {
        let page = bytes.toString('utf8');
        if (!page.includes('<footer><div>')) throw new Error('Expected the reviewed demo footer');
        page = page.replace('<footer><div>', '<footer><div><p><a class="textlink" href="../../index.html">All industry demos</a></p>');
        bytes = Buffer.from(page);
      }
      exports.push({name:`demos/${item.id}/${name}`, bytes});
    }
  }
  index = index.replace('See the repository LICENSE for reuse terms.', '<a href="LICENSE">License and reuse terms</a>.');
  exports.push({name:'index.html', bytes:Buffer.from(index)});
  for (const name of ['catalog.css', 'catalog.js']) exports.push({name,bytes:readFileSync(plainFile(path.join(catalog,name)))});
  for (const name of ['LICENSE', 'NOTICE.md']) exports.push({name,bytes:readFileSync(plainFile(path.join(root,name)))});
  exports.push({name:'robots.txt',bytes:Buffer.from('User-agent: *\nDisallow: /\n')});
  // Validate all input before replacing the previous generated output.
  rmSync(out,{recursive:true,force:true});
  for (const file of exports) {
    const dest = path.join(out,file.name);
    mkdirSync(path.dirname(dest),{recursive:true});
    writeFileSync(dest,file.bytes);
  }
  return exports.map(x=>x.name).sort();
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const files = packageShowcase();
  console.log(`Packaged 14 demos; ${files.length} public files in showcase/.`);
}
