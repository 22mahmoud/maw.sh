import { handleThemeMode } from './handleThemeMode';

import '../styles/main.css';

document.addEventListener('DOMContentLoaded', () => {
  handleThemeMode();
});

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js');
  });
}
