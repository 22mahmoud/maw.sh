import { Configuration } from 'webpack';

const clientProdConfig: Configuration = {
  mode: 'production',

  devtool: 'source-map',

  output: {
    filename: '[name].[chunkhash:8].js',
  },
};

// eslint-disable-next-line import/no-default-export
export default clientProdConfig;
