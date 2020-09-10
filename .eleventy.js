const { format, parseISO } = require('date-fns');
const syntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const Image = require('./eleventy/image');
const collections = require('./eleventy/collections');

const isDev = process.env.NODE_ENV === 'development';

module.exports = (cfg) => {
  cfg.addPassthroughCopy('src/assets/fonts');

  if (isDev) {
    cfg.addPassthroughCopy('src/**/*.jpeg');
    cfg.addPassthroughCopy('src/**/*.jpg');
    cfg.addPassthroughCopy('src/**/*.png');
  }

  cfg.addPassthroughCopy('src/**/*.gif');

  collections(cfg);

  cfg.addFilter('date', (date) => format(parseISO(date), 'd MMMM, yyyy'));

  cfg.addNunjucksAsyncShortcode('Image', Image);

  cfg.addPlugin(syntaxHighlight);

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
