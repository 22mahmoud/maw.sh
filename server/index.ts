import path from 'path';
import express from 'express';
import bodyParser from 'body-parser';
import compression from 'compression';
import morgan from 'morgan';
import helmet from 'helmet';
import { manifestHelper } from './midllewares/manifestMiddleware';

const app = express();

const port = process.env.PORT || 3000;

app.use(compression());

app.set('views', path.join(__dirname, '../', 'web', 'views'));
app.set('view engine', 'pug');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(morgan('dev'));

app.use(
  helmet({
    contentSecurityPolicy: false,
  })
);

app.use(
  express.static(path.join(__dirname, 'public'), { maxAge: 31557600000 })
);

const manifestPath = path.join(__dirname, 'public');

app.use(manifestHelper(`${manifestPath}/manifest.json`));

app.get('/', (_req, res) => {
  res.render('home', { name: 'Mahmoud' });
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`App is running at http://localhost:${port}`);
});
