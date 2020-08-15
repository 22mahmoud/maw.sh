import path from 'path';
import { Configuration } from 'webpack';
import nodeExternals from 'webpack-node-externals';

import { paths } from '../paths';
import { loaders } from './loaders';
import { resolvers } from './resolvers';
import { plugins } from './plugins';

const serverCommonConfig: Configuration = {
  name: 'server',

  target: 'node',

  entry: {
    server: [
      'core-js/stable',
      'regenerator-runtime/runtime',
      path.resolve(paths.srcServer, 'index.ts'),
    ],
  },

  output: {
    path: paths.buildServer,
    filename: 'server.js',
    publicPath: '/',
  },

  externals: [
    nodeExternals({
      allowlist: /\.css$/,
    }),
  ],

  resolve: {
    ...resolvers,
  },

  module: {
    rules: [...loaders.server],
  },

  plugins: [...plugins.shared, ...plugins.server],

  node: {
    __dirname: false,
  },

  stats: {
    assets: false,
    cached: false,
    cachedAssets: false,
    chunks: false,
    chunkModules: false,
    children: false,
    colors: true,
    hash: false,
    modules: false,
    performance: false,
    reasons: false,
    timings: true,
    version: false,
  },
};

// eslint-disable-next-line import/no-default-export
export default serverCommonConfig;
