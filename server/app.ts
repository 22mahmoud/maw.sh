import path from 'path';
import express from 'express';

import { middlewares } from './midllewares';
import { paths } from '../config/paths';

const app = express();

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

  app.get('/', async (_req, res) => {
    res.render('home', {
      title: 'Home',
      name: 'Mahmoud!',
    });
  });

  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`App is running at http://localhost:${port}`);
  });
};
