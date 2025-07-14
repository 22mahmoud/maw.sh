import '@/css/app.css';

import htmx from 'htmx.org';
import 'htmx-ext-preload';

declare global {
  interface Window {
    htmx: typeof htmx;
  }
}

window.htmx = htmx;
