import Lazyload from 'vanilla-lazyload';
import turbolinks from 'turbolinks';

const isProd = process.env.NODE_ENV === 'production';

if (isProd) {
  const lazyload = new Lazyload();

  turbolinks.start();

  document.addEventListener('DOMContentLoaded', () => {
    lazyload.update();
  });

  document.addEventListener('turbolinks:load', () => {
    lazyload.update();
  });

  if ('serviceWorker' in navigator) {
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
}
