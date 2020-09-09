const postcssPresetEnv = require("postcss-preset-env");
const cssnano = require("cssnano");
const postcssImport = require("postcss-import");
const postcssPurgecss = require("@fullhuman/postcss-purgecss");
const rfs = require("rfs/postcss");

const isProd = process.env.NODE_ENV === "production";

const plugins = [
  postcssPresetEnv({
    stage: 3,
    features: {
      "nesting-rules": true,
    },
  }),

  rfs({
    twoDimensional: false,
    baseValue: 20,
    unit: "rem",
    breakpoint: 1200,
    breakpointUnit: "px",
    factor: 10,
    class: false,
    unitPrecision: 6,
    safariIframeResizeBugFix: false,
    remValue: 16,
  }),

  isProd &&
    postcssPurgecss({
      content: ["./src/**/*.njk", "./src/**/*.md"],
      css: ["./src/styles/**/*.css"],
    }),

  isProd && cssnano(),
];

module.exports = {
  plugins: plugins.filter(Boolean),
};
