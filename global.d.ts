import type Alpine from 'alpinejs';
import type htmx from 'htmx.org';

declare global {
  interface Window {
    htmx: typeof htmx;
    Alpine: typeof Alpine;
  }

  interface ImportMetaEnv {
    readonly VITE_RECAPTCHA_SITE_KEY: string;
  }
}
