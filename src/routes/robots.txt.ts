import { Request, Response } from 'express';

interface Rules {
  'User-agent': string;
  Sitemap: string;
  Host: string;
}

const rules: Rules = {
  'User-agent': '*',
  Sitemap: 'https://mahmoudashraf.dev/sitemap.xml',
  Host: 'https://mahmoudashraf.dev',
};

export function get(_req: Request, res: Response) {
  const content = Object.keys(rules).reduce(
    // @ts-ignore
    (acc, next): string => (acc += `${next}: ${rules[next]}\n`),
    ''
  );

  res.setHeader('Content-Type', 'text/plain');
  res.end(content);
}
