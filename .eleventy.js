const collections = require('./eleventy/collections');
const filters = require('./eleventy/filters');
const shortcodes = require('./eleventy/shortcodes');
const plugins = require('./eleventy/plugins');

const isDev = process.env.NODE_ENV === 'development';

module.exports = (cfg) => {
  cfg.addPassthroughCopy('src/assets');
  cfg.addPassthroughCopy('src/**/*.gif');
  cfg.addPassthroughCopy('src/robots.txt');

  if (isDev) {
    cfg.addPassthroughCopy('src/**/*.jpeg');
    cfg.addPassthroughCopy('src/**/*.jpg');
    cfg.addPassthroughCopy('src/**/*.png');
  }

  collections(cfg);

  filters(cfg);

  shortcodes(cfg);

  plugins(cfg);

  return {
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',

    dir: {
      input: 'src',
      output: 'site',
      includes: '_includes',
      layouts: '_layouts',
    },
  };
};
