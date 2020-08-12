import path from 'path';
import { Configuration } from 'webpack';
import TerserPlugin from 'terser-webpack-plugin';
import OptimizeCSSAssetsPlugin from 'optimize-css-assets-webpack-plugin';

import { paths } from '../paths';
import { loaders } from './loaders';
import { resolvers } from './resolvers';
import { plugins } from './plugins';

const clientCommonConfig: Configuration = {
  target: 'web',

  entry: {
    app: [path.join(paths.src, 'js/app.ts')],
  },

  output: {
    path: paths.build,
    // chunkFilename: '[name].[chunkhash:4].js',
  },

  optimization: {
    minimizer: [
      new TerserPlugin({
        // TerserPlugin config is taken entirely from react-scripts
        terserOptions: {
          parse: {
            ecma: 8,
          },
          compress: {
            warnings: false,
            comparisons: false,
            inline: 2,
          },
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
      new OptimizeCSSAssetsPlugin({}),
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

  resolve: {
    ...resolvers,
  },

  module: {
    rules: [...loaders],
  },

  plugins: [...plugins],

  stats: {
    cached: false,
    cachedAssets: false,
    chunks: false,
    chunkModules: false,
    children: false,
    colors: true,
    hash: false,
    modules: false,
    reasons: false,
    timings: true,
    version: false,
  },
};

// eslint-disable-next-line import/no-default-export
export default clientCommonConfig;
