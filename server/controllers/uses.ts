import { Request, Response } from 'express';

import { handleMarkDown } from '../utils/handleMd';

export const getUses = async (_req: Request, res: Response) => {
  const { md, meta } = await handleMarkDown('web/views/uses.md');
  res.render(`templates/markdown`, {
    md,
    meta,
    description: meta.description,
    title: meta.title,
  });
};
