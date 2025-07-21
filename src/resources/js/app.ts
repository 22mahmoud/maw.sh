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
  .from('.hero-image', { opacity: 0, scale: 0.95, rotate: -2, duration: 0.8 }, '-=0.4')
  .to('.hero-image', { rotate: 0, filter: 'blur(0px)', duration: 0.4 }, '-=0.6')
  .from('.hero-headline-text', { opacity: 0, y: 20, filter: 'blur(4px)', duration: 0.8 }, '-=0.4')
  .to('.hero-headline-text', { filter: 'blur(0px)', duration: 0.3 }, '-=0.7')
  .from('.hero-subtext', { opacity: 0, y: 20 }, '-=0.4')
  .from('.hero-buttons', { opacity: 0, y: 20, stagger: 0.1 }, '-=0.4')
  .from('.hero-social a', { opacity: 0, y: 20, stagger: 0.1 }, '-=0.4');
