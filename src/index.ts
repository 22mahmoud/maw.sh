import express from 'express';
import bodyParser from 'body-parser';
import compression from 'compression';
import morgan from 'morgan';
import helmet from 'helmet';

const app = express();

const port = process.env.PORT || 8000;

app.use(compression());

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(morgan('dev'));

app.use(helmet());

app.get('/', (_req, res) => {
  res.send('Hello, World');
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`App is running at http://localhost:${port}`);
});
