/* eslint-disable no-console */
import { Configuration, Compiler, MultiCompiler } from 'webpack';
import chalk from 'chalk';

import getClientConfig from '../config/webpack/client.config';
import getServerConfig from '../config/webpack/server.config';

const logColors = {
  error: 'red',
  warning: 'yellow',
  info: 'blue',
};

export const logMessage = (message: string | Error, level = 'info'): void => {
  const color = logColors[level] || 'white';

  console.log(`[${new Date().toISOString()}]`, chalk[color](message));
};

export const getWebpackConfig = async (): Promise<Configuration[]> => {
  let env = 'dev';

  if (process.env.NODE_ENV === 'production') {
    env = 'prod';
  }

  const configs = await Promise.all([
    getClientConfig({ env }),
    getServerConfig({ env }),
  ]);

  return configs;
};

export const getWebpackCompiler = (
  name: string,
  multiCompilers: MultiCompiler
): Compiler => {
  const compiler: Compiler = multiCompilers.compilers.find(
    (c) => c.name === name
  );

  return compiler;
};

export const compilerPromise = (compiler: Compiler) => async (): Promise<
  void
> =>
  new Promise((resolve, reject) => {
    compiler.hooks.compile.tap(compiler.name, () => {
      logMessage(`[${compiler.name}] Compiling `);
    });

    compiler.hooks.done.tap(compiler.name, (stats) => {
      if (!stats.hasErrors()) {
        return resolve();
      }

      return reject(Error(`Failed to compile ${compiler.name}`));
    });

    if (process.env.NODE_ENV === 'production') {
      compiler.watch({}, (error, stats) => {
        if (!error && !stats.hasErrors()) {
          console.log(stats.toString());
          return;
        }
        console.error(chalk.red(stats.compilation.errors));
      });
    }
  });
