const markdownIt = require('markdown-it');
const markdownItAnchor = require('markdown-it-anchor');

const collections = require('./eleventy/collections');
const filters = require('./eleventy/filters');
const shortcodes = require('./eleventy/shortcodes');
const plugins = require('./eleventy/plugins');
const transformers = require('./eleventy/transformers');

const isDev = process.env.NODE_ENV === 'development';

const anchorSlugify = (s) =>
  encodeURIComponent(
    'h-' +
      String(s)
        .trim()
        .toLowerCase()
        .replace(/[.,\/#!$%\^&\*;:{}=_`~()]/g, '')
        .replace(/\s+/g, '-')
  );

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

  transformers(cfg);

  // Markdown Parsing
  cfg.setLibrary(
    'md',
    markdownIt({
      html: true,
      breaks: true,
      typographer: true,
    }).use(markdownItAnchor, {
      permalink: true,
      permalinkSymbol: '🔗',
      permalinkClass: 'heading-anchor',
      permalinkBefore: true,
      level: 2,
      slugify: anchorSlugify,
    })
  );

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
