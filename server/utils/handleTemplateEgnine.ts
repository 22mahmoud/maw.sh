import path from 'path';

import { paths } from '../../config/paths';

export const handleTemplateEngine = async (
  pugPath: string,
  options: object,
  done: (e: any, rendered?: string | undefined) => void
) => {
  try {
    const filepath = path.relative(paths.views, pugPath);

    const { default: template } = await import(`../../web/views/${filepath}`);

    const html = template(options);

    done(null, html);
  } catch (error) {
    done(error);
  }
};
