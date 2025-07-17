import type htmx from 'htmx.org';

declare global {
  interface Window {
    htmx: typeof htmx;
  }

  interface ImportMetaEnv {
    readonly VITE_RECAPTCHA_SITE_KEY: string;
  }
}
