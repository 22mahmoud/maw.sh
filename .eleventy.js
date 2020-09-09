module.exports = (cfg) => {
  cfg.addPassthroughCopy("src/assets/fonts");

  return {
    dir: {
      input: "src",
      output: "site",
      includes: "_includes",
      layouts: "_layouts",
    },
  };
};
