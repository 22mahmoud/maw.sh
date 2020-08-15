import { Configuration } from 'webpack';

const serverDevConfig: Configuration = {
  mode: 'development',
  devServer: {
    writeToDisk: true,
  },
};

// eslint-disable-next-line import/no-default-export
export default serverDevConfig;
