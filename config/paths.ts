import fs from 'fs';
import path from 'path';

const appDirectory: string = fs.realpathSync(process.cwd());

const resolveApp = (relativePath: string): string =>
  path.resolve(appDirectory, relativePath);

export const paths = {
  src: resolveApp('web'),
  build: resolveApp('dist/public'),
};
