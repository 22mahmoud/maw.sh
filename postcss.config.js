const postcssPresetEnv = require('postcss-preset-env');
const cssnano = require('cssnano');
const postcssFunctions = require('postcss-functions');
const color = require('css-color-converter');

const postcssPurgecss = require('@fullhuman/postcss-purgecss');
const rfs = require('rfs/postcss');

const isProd = process.env.NODE_ENV === 'production';

const plugins = [
  postcssPresetEnv({
    stage: 3,
    features: {
      'nesting-rules': true,
      'not-pseudo-class': true,
    },
  }),

  rfs({
    twoDimensional: false,
    baseValue: 20,
    unit: 'rem',
    breakpoint: 1200,
    breakpointUnit: 'px',
    factor: 10,
    class: false,
    unitPrecision: 6,
    safariIframeResizeBugFix: false,
    remValue: 16,
  }),

  postcssFunctions({
    functions: {
      darken: (value, frac) => {
        console.log(value);
        const darken = 1 - parseFloat(frac);
        const [r, g, b] = color(value)
          .toRgbaArray()
          .map((val) => val * darken);

        return color([r, g, b]).toHexString();
      },
    },
  }),
  isProd &&
    postcssPurgecss({
      content: ['./site/**/*.html'],
      css: ['./src/styles/**/*.css'],
    }),

  isProd && cssnano(),
];

module.exports = {
  plugins: plugins.filter(Boolean),
};
