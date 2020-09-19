const { format, parseISO, formatISO } = require('date-fns');

const site = require('../../src/data/site');

module.exports = (cfg) => {
  cfg.addFilter('date', (date) => format(parseISO(date), 'd MMMM, yyyy'));

  cfg.addFilter('iso', (date) => {
    return formatISO(new Date(date));
  });

  cfg.addFilter('time', (date) => {
    return format(parseISO(date), 'h:mm aaa');
  });

  cfg.addFilter('getTitle', (title) =>
    title ? `${title} - ${site.title}` : site.title
  );

  cfg.addFilter(
    'getDescription',
    (description = site.description) => description
  );
};
