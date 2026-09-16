import {mkdir,copyFile,readdir} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
for(const name of await readdir('web'))await copyFile(`web/${name}`,`dist/${name}`);
await copyFile('engine.py','dist/engine.py');
console.log('Built static Pong site in dist/');
