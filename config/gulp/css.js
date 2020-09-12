const { src, dest, watch, series } = require('gulp');
const postcss = require('gulp-postcss');
const postcssFunctions = require('postcss-functions');
const color = require('css-color-converter');
const rfs = require('rfs/postcss');
const postcssImport = require('postcss-import');
const postcssPresetEnv = require('postcss-preset-env');
const cssnano = require('cssnano');
const postcssPurgecss = require('@fullhuman/postcss-purgecss');
const autoprefixer = require('autoprefixer');

const paths = require('../paths');
const { server } = require('./browserSync');

function css() {
  const plugins = [
    postcssImport,
    autoprefixer,
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
    postcssPresetEnv({
      stage: 3,
      features: {
        'nesting-rules': true,
        'not-pseudo-class': true,
      },
    }),

    postcssFunctions({
      functions: {
        darken: (value, frac) => {
          const darken = 1 - parseFloat(frac);
          const [r, g, b] = color(value)
            .toRgbaArray()
            .map((val) => val * darken);

          return color([r, g, b]).toHexString();
        },
      },
    }),
  ];

  return src(paths.css.mainSrc)
    .pipe(postcss(plugins))
    .pipe(dest(paths.css.dest))
    .pipe(server.stream());
}

function cssMinify() {
  const purgecss = postcssPurgecss({
    content: [paths.html.src],
  });

  const plugins = [purgecss, cssnano];

  return src(paths.css.mainDest)
    .pipe(postcss(plugins))
    .pipe(dest(paths.css.dest));
}

function cssWatcher() {
  return watch([paths.css.watch], { ignoreInitial: false }, series(css));
}

module.exports = { css, cssMinify, cssWatcher };
