const { format, parseISO, formatISO } = require('date-fns');

const site = require('../src/_data/site');

module.exports = (cfg) => {
  cfg.addFilter('date', (date) => format(parseISO(date), 'd MMMM, yyyy'));

  cfg.addFilter('iso', (date) => {
    return formatISO(date);
  });

  cfg.addFilter('getTitle', (title) =>
    title ? `${title} - ${site.title}` : site.title
  );

  cfg.addFilter(
    'getDescription',
    (description = site.description) => description
  );
};