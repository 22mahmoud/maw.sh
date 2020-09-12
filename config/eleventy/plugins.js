const eleventyNavigationPlugin = require('@11ty/eleventy-navigation');
const syntaxHighlight = require('@11ty/eleventy-plugin-syntaxhighlight');
const pluginRss = require('@11ty/eleventy-plugin-rss');
const sitemap = require('@quasibit/eleventy-plugin-sitemap');

module.exports = (cfg) => {
  cfg.addPlugin(syntaxHighlight);
  cfg.addPlugin(pluginRss);
  cfg.addPlugin(eleventyNavigationPlugin);

  cfg.addPlugin(sitemap, {
    sitemap: {
      hostname: 'https://www.mahmoudashraf.dev/',
    },
  });
};
