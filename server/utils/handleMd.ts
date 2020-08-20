import path from 'path';
import fs from 'fs';
import grayMatter from 'gray-matter';

import { paths } from '../../config/paths';

export const handleMarkDown = async (mdPath: string) => {
  const filepath = path.relative(paths.views, mdPath);

  let { default: md }: { default: string } = await import(
    `../../web/views/${filepath}`
  );

  md = md.replace(/assets/g, '/assets');

  const rawMd = fs.readFileSync(mdPath);
  const { data: meta } = grayMatter(rawMd);

  return {
    meta,
    md,
  };
};
