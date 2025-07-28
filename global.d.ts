import type Alpine from 'alpinejs';
import type htmx from 'htmx.org';

interface AppData {
  isNewGuestbookPage: boolean;
}

declare global {
  interface Window {
    htmx: typeof htmx;
    Alpine: typeof Alpine;
    djdt: {
      show_toolbar: () => void;
    };
    __APP_DATA__: AppData;
  }

  interface ImportMetaEnv {
    readonly VITE_RECAPTCHA_SITE_KEY: string;
  }
}
