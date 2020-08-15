import { Configuration } from 'webpack';

const clientDevConfig: Configuration = {
  mode: 'development',

  devtool: 'cheap-module-source-map',

  output: {
    filename: '[name].[hash:4].js',
    crossOriginLoading: 'anonymous',
  },
};

// eslint-disable-next-line import/no-default-export
export default clientDevConfig;
