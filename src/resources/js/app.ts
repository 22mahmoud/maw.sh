import '@/css/app.css';

import collapse from '@alpinejs/collapse';
import Alpine from 'alpinejs';
import { gsap } from 'gsap';
import htmx from 'htmx.org';

window.Alpine = Alpine;
window.htmx = htmx;

Alpine.plugin(collapse);
Alpine.start();

const timeline = gsap.timeline({ defaults: { ease: 'power2.out', duration: 0.6 } });

timeline
  .from('.hero-status', { opacity: 0, y: -10 })
  .from('.hero-image', { opacity: 0, scale: 0.95 }, '-=0.4')
  .from('.hero-headline-text', { opacity: 0, y: 20 }, '-=0.3')
  .from('.hero-subtext', { opacity: 0, y: 20 }, '-=0.4')
  .from('.hero-buttons', { opacity: 0, y: 20 }, '-=0.4')
  .from('.hero-social', { opacity: 0, y: 20 }, '-=0.4');
