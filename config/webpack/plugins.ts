import webpack, { Plugin } from 'webpack';
import ManifestPlugin from 'webpack-manifest-plugin';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import CopyPlugin from 'copy-webpack-plugin';
import { paths } from '../paths';

const isDev = () => process.env.NODE_ENV === 'development';

export const plugins: Plugin[] = [
  new MiniCssExtractPlugin({
    filename: isDev() ? '[name].css' : '[name].[contenthash].css',
    chunkFilename: isDev() ? '[id].css' : '[id].[contenthash].css',
  }),

  new ManifestPlugin({ fileName: 'manifest.json' }),

  new CopyPlugin({
    patterns: [{ from: paths.static, to: paths.build }],
  }),

  new webpack.DefinePlugin({
    __SERVER__: 'false',
    __BROWSER__: 'true',
  }),

  isDev() && new webpack.HotModuleReplacementPlugin(),
].filter(Boolean) as Plugin[];
