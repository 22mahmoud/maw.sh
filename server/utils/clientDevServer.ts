import { Express } from 'express';
import webpack from 'webpack';
import webpackDevMiddleware from 'webpack-dev-middleware';

import WebpackHotMiddleware from 'webpack-hot-middleware';
import { paths } from '../../config/paths';
import getWebpackConfig from '../../config/webpack/webpack.config';

const PORT = 3000;
const HOST = 'http://localhost';

export const clientDevServer = async (app: Express) => {
  const webpackConfig = await getWebpackConfig({ env: 'dev' });

  webpackConfig.entry = {
    app: [
      `webpack-hot-middleware/client?path=${HOST}:${PORT}/__webpack_hmr&reload=true`,
      // @ts-ignore
      ...webpackConfig.entry.app,
    ],
  };

  if (webpackConfig.output) {
    webpackConfig.output.hotUpdateMainFilename =
      'updates/[hash].hot-update.json';
    webpackConfig.output.hotUpdateChunkFilename =
      'updates/[id].[hash].hot-update.js';
  }

  const webpackCompiler = webpack(webpackConfig);

  app.use(
    webpackDevMiddleware(webpackCompiler, {
      publicPath: paths.build,
      writeToDisk: true,
    })
  );

  app.use(WebpackHotMiddleware(webpackCompiler));
};
