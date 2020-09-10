const { format, parseISO } = require('date-fns');
const Image = require('./eleventy/image');
const collections = require('./eleventy/collections');

module.exports = (cfg) => {
  cfg.addPassthroughCopy('src/assets/fonts');
  cfg.addPassthroughCopy('src/**/*.gif');

  collections(cfg);

  cfg.addFilter('date', (date) => format(parseISO(date), 'd MMMM, yyyy'));

  cfg.addNunjucksAsyncShortcode('Image', Image);

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
