import '@/css/app.css';

import htmx from 'htmx.org';

declare global {
  interface Window {
    htmx: typeof htmx;
  }
}

window.htmx = htmx;
