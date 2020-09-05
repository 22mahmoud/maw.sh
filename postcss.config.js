/* eslint-disable */
const isProd = process.env.NODE_ENV === 'production';

module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss'),
    require('tailwindcss'),
    isProd &&
      require('cssnano')({
        preset: ['default', { discardComments: { removeAll: true } }],
      }),
  ].filter(Boolean),

  sourceMap: true,
};
