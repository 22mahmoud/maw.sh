const path = require('path');
const htmlmin = require('html-minifier-terser');

const isProd = process.env.NODE_ENV === 'production';

module.exports = (cfg) => {
  cfg.addTransform('htmlmin', (content, outputPath) => {
    if (path.extname(outputPath) !== '.html' || !isProd) return content;

    return htmlmin.minify(content, {
      useShortDoctype: true,
      minifyCSS: true,
      minifyJS: true,
      removeComments: true,
      collapseWhitespace: true,
    });
  });
};
