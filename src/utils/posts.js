import fs from 'fs-extra';
import path from 'path';

export function getPosts() {
  return fs.readdirSync(`content`);
}

export function getPost(filename) {
  const filePath = path.resolve('content', filename);
  const post = fs.readFileSync(filePath, 'utf-8');
  return post;
}
