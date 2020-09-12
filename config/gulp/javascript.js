const { src, dest } = require('gulp');
const webpackStream = require('webpack-stream');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
const ManifestPlugin = require('webpack-manifest-plugin');

const paths = require('../paths');

const isProd = process.env.NODE_ENV === 'production';

const babelConfig = {
  test: /\.m?js$/,
  exclude: /node_modules/,
  use: {
    loader: 'babel-loader',
    options: {
      presets: [
        [
          '@babel/env',
          {
            modules: false,
            useBuiltIns: 'entry',
            corejs: 3.6,
          },
        ],
      ],
      cacheDirectory: true,
      cacheCompression: isProd,
      compact: isProd,
    },
  },
};

const envConfig = new webpack.DefinePlugin({
  'process.env': {
    NODE_ENV: JSON.stringify(process.env.NODE_ENV),
  },
});

const webpackGulp = webpackStream(
  {
    target: 'web',

    entry: { app: paths.js.src },

    watch: !isProd,

    output: {
      path: paths.js.dest,
      filename: isProd ? '[name].[chunkhash:8].js' : '[name].[hash:4].js',
    },

    mode: process.env.NODE_ENV || 'development',

    module: {
      rules: [babelConfig],
    },

    plugins: [
      envConfig,
      new ManifestPlugin({
        publicPath: `/assets/js/`,
      }),
    ],

    optimization: {
      minimizer: [
        new TerserPlugin({
          // TerserPlugin config is taken entirely from react-scripts
          terserOptions: {
            parse: {
              ecma: 8,
            },
            compress: {},
            mangle: {
              safari10: true,
            },
            output: {
              ecma: 5,
              comments: false,
              ascii_only: true,
            },
          },
          parallel: true,
          cache: true,
          sourceMap: true,
        }),
      ],

      namedModules: true,
      noEmitOnErrors: true,
      splitChunks: {
        cacheGroups: {
          commons: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendor',
            chunks: 'all',
          },
        },
      },
    },
  },
  webpack
);

function javascript() {
  return src(paths.js.src).pipe(webpackGulp).pipe(dest(paths.js.dest));
}

module.exports = { javascript };
