import { Request, Response } from 'express';

export const getHome = async (_req: Request, res: Response) => {
  res.render('home', {
    title: 'Home',
  });
};
