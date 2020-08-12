import { merge } from 'webpack-merge';
import { Configuration } from 'webpack';

import commonConfig from './webpack.common';

// eslint-disable-next-line import/no-default-export
export default async ({ env }: { env: string }): Promise<Configuration> => {
  const { default: envConfig } = await import(`./webpack.${env}.ts`);

  return merge(commonConfig, envConfig as Configuration);
};
