import fs from 'fs';
import { Request, Response } from 'express';

import { handleMarkDown } from '../utils/handleMd';

export const getRss = async (_req: Request, res: Response) =>
  res.redirect('/rss.xml');

export const getRssXml = async (_req: Request, res: Response) => {
  res.type('xml');
  const promises: Promise<any>[] = [];

  fs.readdirSync('web/views/blog').forEach((dir) => {
    promises.push(handleMarkDown(`web/views/blog/${dir}/index.md`));
  });

  let posts = await Promise.all(promises);
  posts = posts.map((post) => ({ ...post.meta, content: post.md }));

  res.render('rss', {
    posts,
  });
};
