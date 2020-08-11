const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  target: 'web',

  entry: { app: [path.resolve(__dirname, 'web/js/app.ts')] },

  output: {
    path: path.resolve(__dirname, 'dist/public'),
  },

  resolve: {
    extensions: ['.js', '.json', '.jsx', '.css', '.ts'],
  },

  devtool: 'inline-cheap-module-source-map',

  devServer: {
    writeToDisk: true,
  },

  module: {
    rules: [
      {
        test: /\.(ts|js)x?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        options: {
          cacheDirectory: true,
        },
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
    ],
  },

  plugins: [new MiniCssExtractPlugin()],
};
