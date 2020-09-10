const { format, parseISO } = require('date-fns');
const Image = require('@11ty/eleventy-img');
const sharp = require('sharp');

module.exports = (cfg) => {
  cfg.addPassthroughCopy('src/assets/fonts');

  cfg.addPassthroughCopy('src/**/*.jpg');
  cfg.addPassthroughCopy('src/**/*.jpeg');
  cfg.addPassthroughCopy('src/**/*.gif');
  cfg.addPassthroughCopy('src/**/*.webp');

  cfg.addCollection('latestPosts', function (collectionApi) {
    return collectionApi.getFilteredByTag('posts').reverse().slice(0, 3);
  });

  cfg.addFilter('date', (date) => format(parseISO(date), 'd MMMM, yyyy'));

  cfg.addNunjucksAsyncShortcode('Image', async (src, alt) => {
    if (!alt) {
      throw new Error(`Missing \`alt\` on myImage from: ${src}`);
    }

    let stats = await Image(src, {
      widths: [25, 320, 640, 960, 1200, 1800, 2400],
      formats: ['jpeg', 'webp'],
      urlPath: '/images/',
      outputDir: './site/images/',
    });

    let lowestSrc = stats['jpeg'][0];

    const placeholder = await sharp(lowestSrc.outputPath)
      .resize({ fit: sharp.fit.inside })
      .blur()
      .toBuffer();

    const base64Placeholder = `data:image/png;base64,${placeholder.toString(
      'base64'
    )}`;

    const srcset = Object.keys(stats).reduce(
      (acc, format) => ({
        ...acc,
        [format]: stats[format].reduce(
          (_acc, curr) => `${_acc} ${curr.srcset} ,`,
          ''
        ),
      }),
      {}
    );

    const source = `<source type="image/webp" data-srcset="${srcset['webp']}">`;
    const sourceNoScript = `<source type="image/webp" srcset="${srcset['webp']}">`;

    const img = `<img
      class="lazy"
      loading="lazy"
      alt="${alt}"
      src="${base64Placeholder}"
      data-src="${lowestSrc.url}"
      data-sizes='(min-width: 1024px) 1024px, 100vw'
      data-srcset="${srcset['jpeg']}"
      width="${lowestSrc.width}"
      height="${lowestSrc.height}">`;

    const imgNoScript = `<img
      loading="lazy"
      alt="${alt}"
      src="${base64Placeholder}"
      sizes='(min-width: 1024px) 1024px, 100vw'
      srcset="${srcset['jpeg']}"
      width="${lowestSrc.width}"
      height="${lowestSrc.height}">`;

    return `<picture> ${source} ${img} </picture>
      <noscript>
        <style>
          img.lazy {
            display: none;
          }
        </style>
        <picture> ${sourceNoScript} ${imgNoScript} </picture>
      </noscript>`;
  });

  return {
    templateFormats: ['md', 'njk', 'html'],
    markdownTemplateEngine: 'njk',
    htmlTemplateEngine: 'njk',
    dataTemplateEngine: 'njk',

    dir: {
      input: 'src',
      output: 'site',
      includes: '_includes',
      layouts: '_layouts',
    },
  };
};
