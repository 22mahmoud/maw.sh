import type htmx from 'htmx.org';

declare global {
  interface Window {
    htmx: typeof htmx;
  }

  const grecaptcha: {
    ready: (callback: () => void) => void;
    execute: (siteKey: string, options: { action: string }) => Promise<string>;
  };

  interface ImportMetaEnv {
    readonly VITE_RECAPTCHA_SITE_KEY: string;
  }
}
