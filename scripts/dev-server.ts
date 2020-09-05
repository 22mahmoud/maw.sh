/* eslint-disable no-console */
import webpack, { ICompiler } from 'webpack';
import rimraf from 'rimraf';
import nodemon from 'nodemon';
import express from 'express';
import webpackDevMiddleWare from 'webpack-dev-middleware';
import webpackHotMiddleware from 'webpack-hot-middleware';

import { paths } from '../config/paths';
import {
  getWebpackConfig,
  getWebpackCompiler,
  compilerPromise,
  logMessage,
} from './utils';

const PORT = 8051;
const HOST = 'http://localhost';

const app = express();

const start = async () => {
  const [clientConfig, serverConfig] = await getWebpackConfig();

  clientConfig.entry = {
    app: [
      `webpack-hot-middleware/client?path=${HOST}:${PORT}/__webpack_hmr&reload=true`,
      // @ts-ignore
      ...clientConfig.entry.app,
    ],
  };

  clientConfig.output.hotUpdateMainFilename = 'updates/[hash].hot-update.json';
  clientConfig.output.hotUpdateChunkFilename =
    'updates/[id].[hash].hot-update.js';

  const webpackCompilers = webpack([clientConfig, serverConfig]);

  const clientCompiler = getWebpackCompiler('client', webpackCompilers);
  const serverCompiler = getWebpackCompiler('server', webpackCompilers);

  const clientPromise = compilerPromise(clientCompiler);
  const serverPromise = compilerPromise(serverCompiler);

  const watchOptions: ICompiler.WatchOptions = {
    ignored: /node_modules/,
  };

  app.use(
    webpackDevMiddleWare(clientCompiler, {
      publicPath: clientConfig.output.publicPath,
      stats: clientConfig.stats,
      writeToDisk: true,
      watchOptions,
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    })
  );

  app.use(webpackHotMiddleware(clientCompiler));

  app.listen(PORT);

  serverCompiler.watch(watchOptions, (error, stats) => {
    if (!error && !stats?.hasErrors()) {
      console.log(stats.toString(serverConfig.stats));
      return;
    }

    if (error) {
      logMessage(error, 'error');
    }

    if (stats?.hasErrors()) {
      const info = stats.toJson();
      const errors = info.errors[0].split('\n');
      logMessage(errors[0], 'error');
      logMessage(errors[1], 'error');
      logMessage(errors[2], 'error');
    }
  });

  try {
    await serverPromise();
    await clientPromise();
  } catch (error) {
    logMessage(error, 'error');
  }

  const script = nodemon({
    script: `${paths.buildServer}/server.js`,
    delay: 50,
    ignore: ['dist/public/', 'server/', 'web/', 'scripts/', 'config/'],
  });

  script.on('restart', () => {
    logMessage('Server side app has been restarted.', 'warning');
  });

  script.on('quit', () => {
    console.log('Process ended');
    process.exit();
  });

  script.on('error', () => {
    logMessage('An error occured. Exiting', 'error');
    process.exit(1);
  });
};

rimraf.sync(paths.buildServer);
start();
