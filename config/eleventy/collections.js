module.exports = (cfg) => {
  cfg.addCollection('latestPosts', function (collectionApi) {
    return collectionApi.getFilteredByTag('posts').reverse().slice(0, 3);
  });
};
