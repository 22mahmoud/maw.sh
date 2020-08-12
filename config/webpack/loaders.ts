import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import { RuleSetRule } from 'webpack';

const isProd = process.env.NODE_ENV === 'production';

const cssRegex = /\.css$/;

const babelLoader: RuleSetRule = {
  test: /\.(ts|js)x?$/,
  loader: 'babel-loader',
  exclude: /node_modules/,
  options: {
    cacheDirectory: true,
    cacheCompression: isProd,
    compact: isProd,
  },
};

const cssLoader: RuleSetRule = {
  test: cssRegex,
  exclude: /node_modules/,
  use: [
    MiniCssExtractPlugin.loader,
    'css-loader',
    {
      loader: 'postcss-loader',
      options: {
        sourceMap: true,
      },
    },
  ],
};

const urlLoader: RuleSetRule = {
  test: /\.(png|jpe?g|gif|svg)$/,
  loader: 'url-loader',
  options: {
    limit: 2048,
    name: 'assets/[name].[hash:8].[ext]',
  },
};

const fileLoader: RuleSetRule = {
  exclude: [/\.(js|jsx|ts|tsx|css|mjs|html|ejs|json)$/],
  use: [
    {
      loader: 'file-loader',
      options: {
        name: 'assets/[name].[hash:8].[ext]',
      },
    },
  ],
};

export const loaders: RuleSetRule[] = [
  {
    oneOf: [babelLoader, cssLoader, urlLoader, fileLoader],
  },
];
