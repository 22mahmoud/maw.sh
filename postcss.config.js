const postcssImport = require('postcss-import');
const purgecss = require('@fullhuman/postcss-purgecss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

const { paths } = require('./config/paths');

const production = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    postcssImport({
      path: [paths.src, `node_modules`],
    }),

    autoprefixer(),

    production &&
      purgecss({
        content: [`${paths.src}/**/*.{ts,pug}`],
      }),

    production &&
      cssnano({
        preset: ['default', { discardComments: { removeAll: true } }],
      }),
  ].filter(Boolean),

  sourceMap: true,
};
