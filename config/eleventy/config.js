const fs = require('fs');
const path = require('path');

const appDirectory = fs.realpathSync(process.cwd());

const resolveApp = (relativePath) => path.resolve(appDirectory, relativePath);

const paths = {
  site: resolveApp('dist'),
  images: resolveApp('dist/images'),
};

module.exports = { paths };
