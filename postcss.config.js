const postcssPresetEnv = require("postcss-preset-env");
const cssnano = require("cssnano");
const postcssImport = require("postcss-import");
const postcssPurgecss = require("@fullhuman/postcss-purgecss");

const isProd = process.env.NODE_ENV === "production";

const plugins = [
  postcssPresetEnv({
    stage: 3,
    features: {
      "nesting-rules": true,
    },
  }),

  isProd &&
    postcssPurgecss({
      content: ["./site/**/*.html"],
      css: ["./src/styles/**/*.css"],
    }),

  isProd && cssnano(),
];

module.exports = {
  plugins: plugins.filter(Boolean),
};
