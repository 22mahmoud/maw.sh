import polka from 'polka';
import sirv from 'sirv';
import compression from 'compression';
import * as sapper from '@sapper/server';

import './styles/index.css';
import 'highlight.js/styles/dracula.css';

const { PORT, NODE_ENV } = process.env; // eslint-disable-line no-undef
const dev = NODE_ENV === 'development';

polka() // You can also use Express
  .use(
    compression({ threshold: 0 }),
    sirv('static', { dev }),
    sapper.middleware()
  )
  .listen(PORT, err => {
    if (err) console.log('error', err);
  });
