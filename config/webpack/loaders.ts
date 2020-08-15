import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import { RuleSetRule } from 'webpack';

const isProd = process.env.NODE_ENV === 'production';
const isDev = process.env.NODE_ENV === 'development';

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

const cssLoaderClient: RuleSetRule = {
  test: cssRegex,
  exclude: /node_modules/,
  use: [
    {
      loader: MiniCssExtractPlugin.loader,
      options: {
        sourceMap: true,
        hmr: isDev,
        reloadAll: isDev,
      },
    },
    { loader: 'css-loader', options: { sourceMap: true } },
    {
      loader: 'postcss-loader',
      options: {
        sourceMap: true,
      },
    },
  ],
};

const cssLoaderServer: RuleSetRule = {
  test: cssRegex,
  exclude: /node_modules/,
  use: [MiniCssExtractPlugin.loader, 'css-loader'],
};

const urlLoaderClient: RuleSetRule = {
  test: /\.(png|jpe?g|gif|svg)$/,
  loader: 'url-loader',
  options: {
    limit: 2048,
    name: '[name].[hash:8].[ext]',
    publicPath: 'assets/',
    outputPath: 'assets/',
  },
};

const urlLoaderServer: RuleSetRule = {
  test: /\.(png|jpe?g|gif|svg)$/,
  loader: 'url-loader',
  options: {
    limit: 2048,
    name: '[name].[hash:8].[ext]',
    publicPath: 'assets/',
    outputPath: 'public/assets/',
  },
};

const fileLoaderClient: RuleSetRule = {
  exclude: [/\.(js|jsx|ts|tsx|css|mjs|html|ejs|json|pug)$/],
  use: [
    {
      loader: 'file-loader',
      options: {
        name: '[name].[hash:8].[ext]',
        publicPath: 'assets/',
        outputPath: 'assets/',
      },
    },
  ],
};

const fileLoaderServer: RuleSetRule = {
  exclude: [/\.(js|jsx|ts|tsx|css|mjs|html|ejs|json|pug)$/],
  use: [
    {
      loader: 'file-loader',
      options: {
        name: '[name].[hash:8].[ext]',
        publicPath: 'assets/',
        outputPath: 'public/assets/',
      },
    },
  ],
};

const pugLoader: RuleSetRule = {
  test: /\.pug$/,
  loader: 'pug-loader',
  exclude: /node_modules/,
};

const client: RuleSetRule[] = [
  {
    oneOf: [
      babelLoader,
      cssLoaderClient,
      pugLoader,
      urlLoaderClient,
      fileLoaderClient,
    ],
  },
];

const server: RuleSetRule[] = [
  {
    oneOf: [
      babelLoader,
      cssLoaderServer,
      pugLoader,
      urlLoaderServer,
      fileLoaderServer,
    ],
  },
];

export const loaders = { server, client };
