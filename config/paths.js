const fs = require('fs');
const path = require('path');

const appDirectory = fs.realpathSync(process.cwd());

const resolveApp = (relativePath) => path.resolve(appDirectory, relativePath);

const resolveSrc = (relativePath) =>
  path.resolve(resolveApp('src'), relativePath);

const resolveDist = (relativePath) =>
  path.resolve(resolveApp('dist'), relativePath);

const resolveAssets = (relativePath) =>
  path.resolve(resolveSrc('assets'), relativePath);

const src = resolveApp('src');
const dest = resolveApp('dist');

module.exports = {
  src,

  dest,

  imagesDest: resolveDist('images'),

  eleventy: {
    watch: [resolveSrc('**/*.{njk,md,json,js}'), resolveApp('.eleventy.js')],
  },

  html: {
    src: resolveDist('**/*.html'),
    dest,
  },

  css: {
    src: resolveAssets('styles'),
    dest: resolveDist('assets/styles'),

    mainSrc: resolveAssets('styles/main.css'),
    mainDest: resolveDist('assets/styles/main.css'),

    watch: resolveAssets('styles/**/*.css'),
  },

  js: {
    src: resolveAssets('js/app.js'),
    dest: resolveDist('assets/js'),
    watch: resolveAssets('js/**/*.js'),
  },
};
