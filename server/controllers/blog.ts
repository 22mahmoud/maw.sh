import fs from 'fs';
import grayMatter from 'gray-matter';
import { Request, Response } from 'express';

export const getBlogs = async (_req: Request, res: Response) => {
  const blogs = fs.readdirSync('web/views/blog').map((dir) => {
    const { data } = grayMatter(
      fs.readFileSync(`web/views/blog/${dir}/index.md`)
    );
    return data;
  });

  res.render('blog', {
    title: 'Blog',
    blogs: blogs.sort((a, b) => (new Date(a.date) > new Date(b.date) ? -1 : 1)),
  });
};

export const getBlog = (md: string, meta: { [key: string]: string }) => async (
  _req: Request,
  res: Response
) => {
  res.render(`templates/markdown`, {
    md,
    meta,
    description: meta.description,
    title: meta.title,
  });
};
