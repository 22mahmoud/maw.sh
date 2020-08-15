import fs from 'fs';
import path from 'path';

const appDirectory: string = fs.realpathSync(process.cwd());

const resolveApp = (relativePath: string): string =>
  path.resolve(appDirectory, relativePath);

export const paths = {
  srcWeb: resolveApp('web/'),
  srcServer: resolveApp('server/'),
  buildWeb: resolveApp('dist/public/'),
  buildServer: resolveApp('dist/'),
  static: resolveApp('web/static/'),
  views: resolveApp('web/views/'),
  manifest: resolveApp('dist/public/manifest.json'),
};
