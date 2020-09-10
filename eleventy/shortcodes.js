const Image = require('./image');

module.exports = (cfg) => {
  cfg.addNunjucksAsyncShortcode('Image', Image);
};
