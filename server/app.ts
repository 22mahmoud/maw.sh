import express from 'express';

import { middlewares } from './midllewares/index';
import { paths } from '../config/paths';
import { handleTemplateEngine } from './utils/handleTemplateEgnine';
import { router } from './routes/index';

const app = express();

const port = process.env.PORT || 3000;
export const startServer = async () => {
  // set pug as template engine
  app.set('views', paths.views);
  app.set('view engine', 'pug');
  app.engine('pug', handleTemplateEngine);

  await middlewares(app);

  app.use(router);

  // start the server
  app.listen(port, () => {
    // eslint-disable-next-line no-console
    console.log(`App is running at http://localhost:${port}`);
  });
};
