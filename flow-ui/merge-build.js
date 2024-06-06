import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

// These lines are necessary to get __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const vueDistPath = path.join(__dirname, 'dist');
const docsDistPath = path.join(__dirname, 'docs/.vitepress/dist');
const targetPath = path.join(__dirname, 'deploy');

fs.removeSync(targetPath); // Clean the target directory
fs.copySync(vueDistPath, targetPath); // Copy Vue app build output
fs.copySync(docsDistPath, path.join(targetPath, 'docs')); // Copy VitePress build output

console.log('Merged build outputs to', targetPath);
