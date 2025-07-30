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

Alpine.data('passwordField', () => ({
  show: false,

  toggle() {
    this.show = !this.show;
  },

  get inputType() {
    return this.show ? 'text' : 'password';
  },

  get isVisible() {
    return this.show;
  },

  get isHidden() {
    return !this.show;
  },

  get toggleLabel() {
    return this.show ? 'Hide password' : 'Show password';
  },
}));

if (window.__APP_DATA__?.isNewGuestbookPage) {
  await import('./guestbook-editor');
}

Alpine.start();

htmx.on('htmx:afterSettle', detail => {
  if (typeof window.djdt !== 'undefined' && detail.target instanceof HTMLBodyElement) {
    window.djdt.show_toolbar();
  }
});
