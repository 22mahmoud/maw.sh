import fs from 'fs-extra';
import path from 'path';
import grayMatter from 'gray-matter';

export function getPosts() {
  return fs.readdirSync(`content`).map(fileName => {
    const post = getPost(fileName);
    const { data } = grayMatter(post);
    return data;
  });
}

export function getPost(filename) {
  const filePath = path.resolve('content', filename);
  const post = fs.readFileSync(filePath, 'utf-8');
  return post;
}
