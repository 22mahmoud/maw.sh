import express from 'express';
import nunjucks from 'nunjucks';

import { middlewares } from './midllewares';
import { paths } from '../config/paths';

const app = express();

const port = process.env.PORT || 3000;

export const startServer = async () => {
  // set nunjucks as template engine
  app.set('view engine', 'html');
  nunjucks.configure(paths.views, {
    autoescape: true,
    express: app,
    watch: true,
  });

  await middlewares(app);

  app.get('/', (_req, res) => {
    res.render('home', { name: 'Mahmoud', title: 'Home' });
  });

  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`App is running at http://localhost:${port}`);
  });
};
