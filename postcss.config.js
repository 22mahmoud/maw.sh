const purgecss = require('@fullhuman/postcss-purgecss')({
  content: ['./src/**/*.html', './src/**/*.svelte'],
  whitelistPatterns: [/svelte-/],
  defaultExtractor: content => content.match(/[A-Za-z0-9-_:/]+/g) || [],
});

const production = process.env.NODE_ENV !== 'development';

module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss'),
    require('autoprefixer'),
    require('postcss-fail-on-warn'),
    production && purgecss,
    production &&
      require('cssnano')({
        preset: 'default',
      }),
  ].filter(Boolean),
};
