// import path from 'path';
import express from 'express';
// @ts-ignore
import homePage from '../web/views/home.pug';

import { middlewares } from './midllewares';
import { paths } from '../config/paths';

const app = express();

const port = process.env.PORT || 3000;
export const startServer = async () => {
  // set pug as template engine
  app.set('views', paths.views);
  app.set('view engine', 'pug');

  await middlewares(app);

  app.get('/', async (_req, res) => {
    const html = homePage({
      title: 'Home',
      name: 'Mahmoud',
      ...res.locals,
    });
    res.send(html);
  });

  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`App is running at http://localhost:${port}`);
  });
};
