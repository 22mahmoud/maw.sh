import '../styles/main.css';
// import { handleThemeMode } from './handleThemeMode';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#rss').addEventListener('click', () => {
    // @ts-ignore
    window.goatcounter.count({
      path: 'click-rss',
      title: 'rss hits',
      event: true,
    });
  });
});
