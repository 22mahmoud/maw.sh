require('dotenv').config();
import * as sapper from '@sapper/app';

sapper.start({
  target: document.querySelector('#sapper'),
});
