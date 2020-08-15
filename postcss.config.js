const postcssImport = require('postcss-import');
const purgecss = require('@fullhuman/postcss-purgecss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');

const production = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    postcssImport({
      path: [`${__dirname}/web`, `node_modules`],
    }),

    autoprefixer(),

    production &&
      purgecss({
        content: [`${__dirname}/web/**/*.{ts,html}`],
      }),

    production &&
      cssnano({
        preset: ['default', { discardComments: { removeAll: true } }],
      }),
  ].filter(Boolean),

  sourceMap: true,
};
