import path from 'path';
import webpack, { Plugin } from 'webpack';
import ManifestPlugin from 'webpack-manifest-plugin';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import CopyPlugin from 'copy-webpack-plugin';
import { GenerateSW } from 'workbox-webpack-plugin';

import WebpackPwaManifest from 'webpack-pwa-manifest';

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

const client = [
  new ManifestPlugin({ fileName: 'manifest-app.json' }),

  new GenerateSW({
    clientsClaim: true,
    skipWaiting: true,
    sourcemap: true,
  }),

  new WebpackPwaManifest({
    background_color: '#1a202c',
    theme_color: '#1a202c',
    name: 'Mahmoud Ashraf',
    short_name: 'Mahmoud Ashraf',
    display: 'standalone',
    start_url: '/',
    fingerprints: false,
    icons: [
      {
        src: path.resolve('web/assets/images/site-logo.png'),
        sizes: [96, 128, 192, 256, 384, 512],
      },
      {
        src: path.resolve('web/assets/images/site-logo.png'),
        size: '1024x1024',
        // @ts-ignore
        purpose: 'maskable',
      },
    ],
  }),
] as Plugin[];

const server = [] as Plugin[];

export const plugins = {
  shared: shared.filter(Boolean),
  client: client.filter(Boolean),
  server: server.filter(Boolean),
};
