const postcssImport = require('postcss-import');
const autoprefixer = require('autoprefixer');
const { paths } = require('./config/paths');

module.exports = {
  plugins: [
    postcssImport({
      path: [paths.src, `${__dirname}/node_modules`],
    }),

    autoprefixer(),
  ],

  sourceMap: true,
};
