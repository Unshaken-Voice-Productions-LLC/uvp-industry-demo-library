const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..');
const build=()=>import(pathToFileURL(path.join(root,'tools/package_showcase.mjs')).href);
function fixture(){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'uvp-showcase-'));
  for(const name of ['03_RECONSTRUCTED_SITES','07_PORTFOLIO_INDEX','LICENSE','NOTICE.md']) fs.cpSync(path.join(root,name),path.join(dir,name),{recursive:true});
  return dir;
}
test('export serves exactly the gallery, 14 demos and legal/robots files',async()=>{
  const dir=fixture();
  try{
    fs.mkdirSync(path.join(dir,'01_INVENTORY'));fs.writeFileSync(path.join(dir,'01_INVENTORY','private.json'),'not for export');
    fs.writeFileSync(path.join(dir,'.env'),'DEMO_ONLY_VALUE=not-for-export');
    const {packageShowcase}=await build();const files=packageShowcase(dir);
    assert.equal(files.length,48);
    assert.equal(files.filter(x=>x.endsWith('.html')).length,15);
    assert.ok(files.every(x=>x.startsWith('demos/')||['index.html','catalog.css','catalog.js','LICENSE','NOTICE.md','robots.txt'].includes(x)));
    assert.ok(!fs.existsSync(path.join(dir,'showcase','01_INVENTORY')));
    assert.ok(!fs.existsSync(path.join(dir,'showcase','.env')));
    const index=fs.readFileSync(path.join(dir,'showcase','index.html'),'utf8');assert.ok(!index.includes('../03_RECONSTRUCTED_SITES'));
    assert.ok(index.includes('href="demos/aleph-motor-works/index.html"'));
    const page=fs.readFileSync(path.join(dir,'showcase','demos/aleph-motor-works/index.html'),'utf8');assert.ok(page.includes('href="../../index.html"'));
    assert.deepEqual(packageShowcase(dir),files);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('manifest traversal is rejected before replacing a good output',async()=>{
  const dir=fixture();
  try{
    const {packageShowcase}=await build();packageShowcase(dir);
    const manifest=path.join(dir,'07_PORTFOLIO_INDEX','portfolio.json');const items=JSON.parse(fs.readFileSync(manifest,'utf8'));
    items[0].demoPath='../../private/index.html';fs.writeFileSync(manifest,JSON.stringify(items));
    assert.throws(()=>packageShowcase(dir),/boundary/);
    assert.ok(fs.existsSync(path.join(dir,'showcase','index.html')));
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('a symlinked demo asset cannot expose unrelated files',async()=>{
  const dir=fixture();
  try{
    const file=path.join(dir,'03_RECONSTRUCTED_SITES/automotive/aleph-motor-works/dist/script.js');fs.unlinkSync(file);fs.symlinkSync(path.join(dir,'NOTICE.md'),file);
    const {packageShowcase}=await build();assert.throws(()=>packageShowcase(dir),/regular source file/);
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
});
test('a symlinked distribution parent cannot escape the export boundary',async()=>{
  const dir=fixture();const outside=fs.mkdtempSync(path.join(os.tmpdir(),'uvp-showcase-private-'));
  try{
    const demo=path.join(dir,'03_RECONSTRUCTED_SITES/automotive/aleph-motor-works/dist');fs.cpSync(demo,outside,{recursive:true});fs.rmSync(demo,{recursive:true});fs.symlinkSync(outside,demo,'dir');
    const {packageShowcase}=await build();assert.throws(()=>packageShowcase(dir),/symlinks/);
  }finally{fs.rmSync(dir,{recursive:true,force:true});fs.rmSync(outside,{recursive:true,force:true});}
});
