const markdownIt = require('markdown-it');
const markdownItAnchor = require('markdown-it-anchor');

const collections = require('./config/eleventy/collections');
const filters = require('./config/eleventy/filters');
const shortcodes = require('./config/eleventy/shortcodes');
const plugins = require('./config/eleventy/plugins');
const transformers = require('./config/eleventy/transformers');

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
  cfg.addPassthroughCopy({ 'src/assets/fonts': 'fonts' });
  cfg.addPassthroughCopy('src/**/*.{gif,svg}');

  cfg.addPassthroughCopy('src/assets/images');
  cfg.addPassthroughCopy('src/assets/favicon.ico');
  cfg.addPassthroughCopy('src/assets/manifest.json');
  cfg.addPassthroughCopy('src/**/*.gif');
  cfg.addPassthroughCopy('src/robots.txt');

  if (process.env.NODE_ENV === 'development') {
    cfg.addPassthroughCopy('src/**/*.{jpg,jpeg,png,webp}');
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
