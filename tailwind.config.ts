import type { Config } from 'tailwindcss';

const config: Config = {
  theme: {
    extend: {
      typography: () => ({
        main: {
          css: {
            '--tw-prose-body': 'var(--color-primary)',
            '--tw-prose-headings': 'var(--color-white)',
            '--tw-prose-lead': 'var(--color-accent)',
            '--tw-prose-links': 'var(--color-accent)',
            '--tw-prose-bold': 'var(--color-white)',
            '--tw-prose-counters': 'var(--color-stuble)',
            '--tw-prose-bullets': 'var(--color-accent)',
            '--tw-prose-hr': 'var(--color-neutral-700)',
            '--tw-prose-quotes': 'var(--color-secondary)',
            '--tw-prose-quote-borders': 'var(--color-neutral-800)',
            '--tw-prose-captions': 'var(--color-stuble)',
            '--tw-prose-code': 'var(--color-accent)',
            '--tw-prose-pre-code': 'var(--color-white)',
            '--tw-prose-pre-bg': 'var(--color-darker)',
            '--tw-prose-th-borders': 'var(--color-neutral-700)',
            '--tw-prose-td-borders': 'var(--color-neutral-800)',

            // Light/inverted mode
            '--tw-prose-invert-body': 'var(--color-primary)',
            '--tw-prose-invert-headings': 'var(--color-dark)',
            '--tw-prose-invert-lead': 'var(--color-accent-bright)',
            '--tw-prose-invert-links': 'var(--color-accent-bright)',
            '--tw-prose-invert-bold': 'var(--color-dark)',
            '--tw-prose-invert-counters': 'var(--color-secondary)',
            '--tw-prose-invert-bullets': 'var(--color-accent)',
            '--tw-prose-invert-hr': 'var(--color-neutral-800)',
            '--tw-prose-invert-quotes': 'var(--color-primary)',
            '--tw-prose-invert-quote-borders': 'var(--color-neutral-800)',
            '--tw-prose-invert-captions': 'var(--color-primary)',
            '--tw-prose-invert-code': 'var(--color-accent)',
            '--tw-prose-invert-pre-code': 'var(--color-white)',
            '--tw-prose-invert-pre-bg': 'rgb(0 0 0 / 5%)', // lighter background
            '--tw-prose-invert-th-borders': 'var(--color-neutral-700)',
            '--tw-prose-invert-td-borders': 'var(--color-neutral-800)',
          },
        },
      }),
    },
  },
};

export default config;
