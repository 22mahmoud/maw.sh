import '../styles/base/fonts.css';
import '../styles/base/normalize.css';
import '../styles/base/typography.css';

import '../styles/utils/variables.css';

import '../styles/vendor/prismjs.css';

import '../styles/components/hero.css';
import '../styles/components/blogs.css';
import '../styles/components/header.css';
import '../styles/components/markdown.css';
import '../styles/components/container.css';

import Lazyload from 'vanilla-lazyload';
import turbolinks from 'turbolinks';

const lazyload = new Lazyload();

turbolinks.start();

document.addEventListener('DOMContentLoaded', () => {
  lazyload.update();
});

document.addEventListener('turbolinks:load', () => {
  lazyload.update();
});

const isProd = process.env.NODE_ENV === 'production';

if (isProd && 'serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      /* eslint-disable */
      .then(() => {
        console.log('sw.js is loaded');
      })
      .catch((error) => {
        console.error(error);
      });
    /* eslint-enable */
  });
}
