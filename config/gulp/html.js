const { src, dest } = require('gulp');
const htmlmin = require('gulp-htmlmin');

const paths = require('../paths');

function htmlMinify() {
  return src(paths.html.src)
    .pipe(htmlmin({ collapseWhitespace: true, removeComments: true }))
    .pipe(dest(paths.html.dest));
}

module.exports = {
  htmlMinify,
};
