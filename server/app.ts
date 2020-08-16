import fs from 'fs';
import path from 'path';
import express from 'express';
import grayMatter from 'gray-matter';

import { middlewares } from './midllewares';
import { paths } from '../config/paths';

const app = express();

const handleMarkDown = async (mdPath: string) => {
  const filepath = path.relative(paths.views, mdPath);

  let { default: md }: { default: string } = await import(
    `../web/views/${filepath}`
  );
  md = md.replace(/src="assets/g, 'src="/assets');
  md = md.replace(/src=assets/g, 'src=/assets');

  const rawMd = fs.readFileSync(mdPath);
  const { data: meta } = grayMatter(rawMd);

  return {
    meta,
    md,
  };
};

const port = process.env.PORT || 3000;
export const startServer = async () => {
  // set pug as template engine
  app.set('views', paths.views);
  app.set('view engine', 'pug');

  app.engine('pug', async (pugPath, options, done) => {
    try {
      const filepath = path.relative(paths.views, pugPath);

      const { default: template } = await import(`../web/views/${filepath}`);

      const html = template(options);

      done(null, html);
    } catch (error) {
      done(error);
    }
  });

  await middlewares(app);

  // Home Pahe
  app.get('/', (_req, res) => {
    res.render('home', {
      title: 'Home',
    });
  });

  // Home Pahe
  app.get('/blog', (_req, res) => {
    const blogs = fs.readdirSync('web/views/blog').map((dir) => {
      const { data } = grayMatter(
        fs.readFileSync(`web/views/blog/${dir}/index.md`)
      );
      return data;
    });
    res.render('blog', {
      title: 'Blog',
      blogs,
    });
  });

  app.get('/about', async (_req, res) => {
    const { md, meta } = await handleMarkDown('web/views/about.md');
    res.render(`templates/markdown`, {
      md,
      meta,
      description: meta.description,
      title: meta.title,
    });
  });

  app.get('/uses', async (_req, res) => {
    const { md, meta } = await handleMarkDown('web/views/uses.md');
    res.render(`templates/markdown`, {
      md,
      meta,
      description: meta.description,
      title: meta.title,
    });
  });

  // blog posts
  const dirs = fs.readdirSync(path.join(paths.views, 'blog'));
  dirs.forEach(async (dir) => {
    const { md, meta } = await handleMarkDown(`web/views/blog/${dir}/index.md`);

    app.get(`/blog/${dir}`, (_req, res) => {
      res.render(`templates/markdown`, {
        md,
        meta,
        description: meta.description,
        title: meta.title,
      });
    });
  });

  // start the server
  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`App is running at http://localhost:${port}`);
  });
};
