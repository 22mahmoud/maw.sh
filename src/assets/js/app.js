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
