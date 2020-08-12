import path from 'path';
import express from 'express';
import compression from 'compression';
import morgan from 'morgan';
import helmet from 'helmet';
import { manifestHelper } from './midllewares/manifestMiddleware';

const app = express();

const port = process.env.PORT || 3000;

app.use(compression());

app.set('views', path.join(__dirname, '../', 'web', 'views'));
app.set('view engine', 'pug');

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(morgan('dev'));

app.use(
  helmet({
    contentSecurityPolicy: false,
  })
);

const publicPath = path.join(__dirname, 'public');

app.use(express.static(publicPath, { maxAge: 31557600000 }));

app.use(manifestHelper(`${publicPath}/manifest.json`));

app.get('/', (_req, res) => {
  res.render('home', { name: 'Mahmoud' });
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`App is running at http://localhost:${port}`);
});
