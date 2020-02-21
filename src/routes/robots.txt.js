const rules = {
  UserAgent: '*',
  Disallow: '/',
  Sitemap: 'https://mahmoudashraf.dev/sitemap.xml',
};

export function get(req, res) {
  res.setHeader('Content-Type', 'text/plain');
  const content = Object.keys(rules).reduce(
    (acc, next) => (acc += `${next}: ${rules[next]}\n`),
    ''
  );

  res.end(content);
}
