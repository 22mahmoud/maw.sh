import '@/css/app.css';

import collapse from '@alpinejs/collapse';
import Alpine from 'alpinejs';
import htmx from 'htmx.org';

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.plugin(collapse);

import '@/js/header-nav';
import '@/js/messages';
import '@/js/django-comments';

if (window.__APP_DATA__?.isNewGuestbookPage) {
  await import('./guestbook-editor');
}

Alpine.start();
