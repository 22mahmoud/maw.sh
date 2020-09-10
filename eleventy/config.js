const fs = require('fs');
const path = require('path');

const appDirectory = fs.realpathSync(process.cwd());

const resolveApp = (relativePath) => path.resolve(appDirectory, relativePath);

const paths = {
  site: resolveApp('site'),
  images: resolveApp('site/images'),
};

module.exports = { paths };
