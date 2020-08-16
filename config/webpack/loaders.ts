import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import { RuleSetRule } from 'webpack';
import RemarkFrontmatter from 'remark-frontmatter';
import RemarkHTML from 'remark-html';
import RemarkHighlightjs from 'remark-highlight.js';
import RemarkOEmbed from '@agentofuser/remark-oembed';

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
  test: /\.(png|jpe?g|gif|svg|webp)$/,
  loader: 'url-loader',
  options: {
    limit: 2048,
    name: '[name].[hash:8].[ext]',
    publicPath: 'assets/',
    outputPath: 'assets/',
  },
};

const urlLoaderServer: RuleSetRule = {
  test: /\.(png|jpe?g|gif|svg|webp)$/,
  loader: 'url-loader',
  options: {
    limit: 2048,
    name: '[name].[hash:8].[ext]',
    publicPath: 'assets/',
    outputPath: 'public/assets/',
    fallback: require.resolve('responsive-loader'),
    // eslint-disable-next-line
    adapter: require('responsive-loader/sharp'),
    placeholder: true,
    sizes: [320, 640, 960, 1200, 1800, 2400],
  },
};

const fileLoaderClient: RuleSetRule = {
  exclude: [/\.(js|jsx|ts|tsx|css|mjs|html|ejs|json|pug|md)$/],
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
  exclude: [/\.(js|jsx|ts|tsx|mjs|html|ejs|json|pug|md)$/],
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
  exclude: /node_modules/,
  use: [
    {
      loader: 'pug-loader',
    },
  ],
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
      {
        test: /\.md$/,
        use: [
          {
            loader: 'html-loader',
            options: {
              // preprocessor: (content, loaderContext) => {
              //   console.log({ content, loaderContext });
              // },

              attributes: {
                list: [
                  {
                    tag: 'img',
                    attribute: 'src',
                    type: 'src',
                  },
                  {
                    tag: 'img',
                    attribute: 'srcset',
                    type: 'srcset',
                  },
                ],
              },
            },
          },
          {
            loader: 'remark-loader',
            options: {
              removeFrontMatter: false,
              remarkOptions: {
                plugins: [
                  RemarkOEmbed,
                  RemarkFrontmatter,
                  RemarkHighlightjs,
                  RemarkHTML,
                ],
                settings: {},
              },
            },
          },
        ],
      },
      pugLoader,
      urlLoaderServer,
      fileLoaderServer,
    ],
  },
];

export const loaders = { server, client };
