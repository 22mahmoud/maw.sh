/* eslint-disable @typescript-eslint/no-var-requires */
/* eslint-disable global-require */
const { paths } = require('./config/paths');

const production = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    require('postcss-import')({
      path: [paths.src, `${__dirname}/node_modules`],
    }),

    require('autoprefixer')(),

    production &&
      require('cssnano')({
        preset: ['default', { discardComments: { removeAll: true } }],
      }),
  ].filter(Boolean),

  sourceMap: true,
};
