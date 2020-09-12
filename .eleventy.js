const markdownIt = require('markdown-it');
const markdownItAnchor = require('markdown-it-anchor');

const collections = require('./config/eleventy/collections');
const filters = require('./config/eleventy/filters');
const shortcodes = require('./config/eleventy/shortcodes');
const plugins = require('./config/eleventy/plugins');
const transformers = require('./config/eleventy/transformers');

const manifest = require('./dist/assets/js/manifest.json');

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
  cfg.addPassthroughCopy('src/assets/fonts');
  cfg.addPassthroughCopy('src/assets/images');
  cfg.addPassthroughCopy('src/assets/favicon.ico');
  cfg.addPassthroughCopy('src/assets/manifest.json');
  cfg.addPassthroughCopy('src/**/*.gif');
  cfg.addPassthroughCopy('src/robots.txt');

  if (isDev) {
    cfg.addPassthroughCopy('src/**/*.jpeg');
    cfg.addPassthroughCopy('src/**/*.jpg');
    cfg.addPassthroughCopy('src/**/*.png');
  }

  collections(cfg);

  filters(cfg);

  /* Filters */
  cfg.addFilter('jsAsset', (name) => {
    return manifest[name];
  });

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
    // use nunjucks as the main template engine.
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',

    // change default inputs and output directories.
    dir: {
      input: 'src',
      output: 'dist',
      includes: 'includes',
      layouts: 'layouts',
      data: 'data',
    },
  };
};
