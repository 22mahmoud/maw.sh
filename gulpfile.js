const { parallel, series } = require('gulp');
const rimraf = require('rimraf');

const paths = require('./config/paths');
const { css, cssMinify, cssWatcher } = require('./config/gulp/css');
const { eleventyWatcher, eleventyBuild } = require('./config/gulp/eleventy');
const { browserSync } = require('./config/gulp/browserSync');
const { htmlMinify } = require('./config/gulp/html');
const { javascript } = require('./config/gulp/javascript');
const { generateSW } = require('./config/gulp/workbox');

function clean(cb) {
  rimraf.sync(paths.dest);
  cb();
}

const dev = series(
  clean,
  parallel(browserSync, eleventyWatcher, cssWatcher, javascript)
);

const build = series(
  clean,
  javascript,
  eleventyBuild,
  parallel(css, htmlMinify),
  cssMinify,
  generateSW
);

module.exports = {
  dev,
  build,
};
