import { Configuration } from 'webpack';

const clientDevConfig: Configuration = {
  mode: 'development',

  devtool: 'cheap-module-source-map',

  devServer: {
    proxy: {
      '/__webpack_hmr': {
        target: 'http://localhost:3000',
        pathRewrite: { '^/__webpack_hmr': '' },
      },
    },
  },

  output: {
    filename: '[name].[hash:4].js',
    crossOriginLoading: 'anonymous',
  },
};

// eslint-disable-next-line import/no-default-export
export default clientDevConfig;
