const { handleImage } = require('./image');

module.exports = (cfg) => {
  cfg.addNunjucksAsyncShortcode('Image', handleImage);
};
