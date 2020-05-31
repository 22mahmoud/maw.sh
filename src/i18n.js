import { register, init, getLocaleFromNavigator } from 'svelte-i18n';

export default function initI18n() {
  register('en', () => import('../locale/en.json'));
  register('ar', () => import('../locale/ar.json'));

  init({
    fallbackLocale: 'en',
    initialLocale: getLocaleFromNavigator(),
  });
}
