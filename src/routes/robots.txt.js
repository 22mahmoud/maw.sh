const rules = {
  'User-agent': '*',
  Sitemap: 'https://mahmoudashraf.dev/sitemap.xml',
  Host: 'https://mahmoudashraf.dev',
};

export function get(req, res) {
  res.setHeader('Content-Type', 'text/plain');
  const content = Object.keys(rules).reduce(
    (acc, next) => (acc += `${next}: ${rules[next]}\n`),
    ''
  );

  res.end(content);
}
