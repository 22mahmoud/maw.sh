import fs from 'fs';
import path from 'path';
import { Router } from 'express';

import { paths } from '../../config/paths';

import { handleMarkDown } from '../utils/handleMd';
import { getHome } from '../controllers/home';
import { getRss, getRssXml } from '../controllers/rss';
import { getBlog, getBlogs } from '../controllers/blog';
import { getAbout } from '../controllers/about';
import { getUses } from '../controllers/uses';

const router = Router();

router.get('/', getHome);

router.get('/rss', getRss);
router.get('/rss.xml', getRssXml);

router.get('/blog', getBlogs);

// retrive all blogs and dynamiclly import it
const dirs = fs.readdirSync(path.join(paths.views, 'blog'));
dirs.forEach(async (dir) => {
  // eslint-disable-next-line
  let { md, meta } = await handleMarkDown(`web/views/blog/${dir}/index.md`);
  let cover: string = '';

  if (meta.cover) {
    const coverPath = path.resolve(
      path.relative(`${paths.views}/blog/${dir}`, meta.cover)
    );

    cover = await import(`../../web/views/blog/${dir}${coverPath}?width=1200`);
    // @ts-ignore
    const srcSet = cover.srcSet?.split(',');
    [cover] = srcSet[srcSet.length - 1].split(' ');
  }

  meta = { ...meta, cover };

  router.get(`/blog/${dir}`, getBlog(md, meta));
});

router.get('/about', getAbout);

router.get('/uses', getUses);

export { router };
