import webpack, { Plugin } from 'webpack';
import ManifestPlugin from 'webpack-manifest-plugin';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import CopyPlugin from 'copy-webpack-plugin';

import { paths } from '../paths';

const isDev = () => process.env.NODE_ENV === 'development';

const shared = [
  new MiniCssExtractPlugin({
    filename: isDev() ? '[name].css' : '[name].[contenthash].css',
    chunkFilename: isDev() ? '[id].css' : '[id].[contenthash].css',
  }),

  new CopyPlugin({
    patterns: [{ from: paths.static, to: paths.buildWeb }],
  }),

  isDev() && new webpack.HotModuleReplacementPlugin(),
] as Plugin[];

const client = [new ManifestPlugin({ fileName: 'manifest.json' })] as Plugin[];

const server = [] as Plugin[];

export const plugins = {
  shared: shared.filter(Boolean),
  client: client.filter(Boolean),
  server: server.filter(Boolean),
};
