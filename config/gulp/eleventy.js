const { spawn } = require('child_process');
const { watch, series } = require('gulp');
const paths = require('../paths');
const { reload } = require('./browserSync');

function build(env) {
  return () =>
    spawn(`NODE_ENV=${env} yarn`, ['eleventy'], {
      shell: true,
      stdio: 'inherit',
    });
}

function eleventyWatcher() {
  return watch(
    paths.eleventy.watch,
    { ignoreInitial: false },
    series(build('development'), reload)
  );
}

module.exports = {
  eleventyWatcher,
  eleventyBuild: build('production'),
};
