import fs from 'fs';

export const generateSitePaths = () => {
  const homePage = {
    path: '/',
    priority: '0.5',
    changefreq: 'monthly',
  };

  const usesPage = {
    path: '/uses',
    priority: '0.6',
    changefreq: 'monthly',
  };

  const aboutPage = {
    path: '/about',
    priority: '0.7',
    changefreq: 'monthly',
  };

  const blogsPage = {
    path: '/blog',
    priority: '1',
    changefreq: 'weekly',
  };

  const blogPages = fs.readdirSync('web/views/blog').map((dir) => ({
    path: `/blog/${dir}`,
    priority: '1',
    changefreq: 'monthly',
  }));

  return [homePage, usesPage, aboutPage, blogsPage, ...blogPages];
};
