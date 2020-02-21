import fs from 'fs-extra';
import siteMetadata from '../../config/siteMetaData';
import { getPosts } from '../utils/posts';

const { siteUrl } = siteMetadata;
const pages = [''];

fs.readdirSync('src/routes').map(file => {
  file = file.split('.')[0];
  if (
    file.charAt(0) !== '_' &&
    file !== 'sitemap' &&
    file !== 'index' &&
    file !== 'robots'
  ) {
    pages.push(file);
  }
});

const render = (pages, posts) => `<?xml version="1.0" encoding="UTF-8" ?>
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
  ${pages
    .map(
      page => `
    <url><loc>${siteUrl}${page}</loc><priority>0.85</priority></url>
  `
    )
    .join('\n')}
  ${posts
    .map(
      post => `
    <url>
      <loc>${siteUrl}blog/${post.slug}</loc>
      <priority>0.69</priority>
    </url>
  `
    )
    .join('\n')}
</urlset>
`;

export async function get(_, res) {
  res.setHeader('Cache-Control', `max-age=0, s-max-age=${600}`); // 10 minutes
  res.setHeader('Content-Type', 'application/rss+xml');
  const posts = getPosts();
  const sitemap = render(pages, posts);
  res.end(sitemap);
}
