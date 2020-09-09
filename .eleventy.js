module.exports = (cfg) => {
  cfg.addPassthroughCopy("src/assets/fonts");

  cfg.addPassthroughCopy("src/**/*.jpg");
  cfg.addPassthroughCopy("src/**/*.jpeg");
  cfg.addPassthroughCopy("src/**/*.gif");

  cfg.addCollection("latestPosts", function(collectionApi) {
    return collectionApi
      .getFilteredByTag("posts")
      .reverse()
      .slice(0, 4);
  });

  return {
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk",

    dir: {
      input: "src",
      output: "site",
      includes: "_includes",
      layouts: "_layouts",
    },
  };
};
