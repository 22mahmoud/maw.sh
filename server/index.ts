import express from 'express';
import compression from 'compression';
import morgan from 'morgan';
import helmet from 'helmet';
import { manifestHelper } from './midllewares/manifestMiddleware';
import { paths } from '../config/paths';
import { clientDevServer } from './utils/clientDevServer';

const app = express();

const port = process.env.PORT || 3000;
const isDev = process.env.NODE_ENV === 'development';

// eslint-disable-next-line @typescript-eslint/no-unused-expressions
isDev && clientDevServer(app);

app.use(compression());

app.set('views', paths.views);
app.set('view engine', 'pug');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(morgan('dev'));

app.use(
  helmet({
    contentSecurityPolicy: false,
  })
);

app.use(express.static(paths.build, { maxAge: 31557600000 }));

app.use(manifestHelper(`${paths.build}/manifest.json`));

app.use((_req, res, next) => {
  res.locals.meta = {
    defaultTitle: 'Mahmoud Ashraf',
    defaultDescription: "Mahmoud Ashraf's sapce on the internet.",
  };

  next();
});

app.get('/', (_req, res) => {
  res.render('home', { name: 'Mahmoud', title: 'Home' });
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`App is running at http://localhost:${port}`);
});
