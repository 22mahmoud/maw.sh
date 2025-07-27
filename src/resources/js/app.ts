import '@/css/app.css';

import collapse from '@alpinejs/collapse';
import Alpine from 'alpinejs';
import htmx from 'htmx.org';

window.Alpine = Alpine;
window.htmx = htmx;

import '@/js/header-nav';
import '@/js/messages';

Alpine.plugin(collapse);

if (window.__APP_DATA__?.isNewGuestbookPage) {
  await import('./guestbook-editor');
}

Alpine.start();
