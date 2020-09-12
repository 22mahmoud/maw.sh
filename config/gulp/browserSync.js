const paths = require('../paths');

const server = require('browser-sync').create();

function reload(cb) {
  server.reload();

  cb();
}

function browserSync() {
  return server.init({
    watch: false,
    open: false,
    notify: false,

    server: {
      baseDir: paths.dest,
    },
  });
}

module.exports = {
  browserSync,
  reload,
  server,
};
