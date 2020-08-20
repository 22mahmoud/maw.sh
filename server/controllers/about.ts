import { Request, Response } from 'express';

import { handleMarkDown } from '../utils/handleMd';

export const getAbout = async (_req: Request, res: Response) => {
  const { md, meta } = await handleMarkDown('web/views/about.md');
  res.render(`templates/markdown`, {
    md,
    meta,
    description: meta.description,
    title: meta.title,
  });
};
