import fs from "fs-extra";
import path from "path";
import grayMatter from "gray-matter";
import { IPostMeta } from "../IPost";

export function getPosts(): IPostMeta[] {
  return fs.readdirSync(`src/content`).map((fileName) => {
    const post = getPost(`${fileName}/index.md`);
    const { data } = grayMatter(post);
    return data as IPostMeta;
  });
}

export function getPost(filename: string) {
  const filePath = path.resolve("src/content", filename);
  const post = fs.readFileSync(filePath, "utf-8");
  return post;
}
