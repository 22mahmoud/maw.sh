const Image = require('@11ty/eleventy-img');
const sharp = require('sharp');

const paths = require('../paths');

const isDev = process.env.NODE_ENV === 'development';

async function getPlaceHolder(outputPath) {
  const placeholder = await sharp(outputPath)
    .resize({ fit: sharp.fit.inside })
    .blur()
    .toBuffer();

  return `data:image/png;base64,${placeholder.toString('base64')}`;
}

function generateSrcset(stats) {
  return Object.keys(stats).reduce(
    (acc, format) => ({
      ...acc,
      [format]: stats[format].reduce(
        (_acc, curr) => `${_acc} ${curr.srcset} ,`,
        ''
      ),
    }),
    {}
  );
}

module.exports = async (src, alt) => {
  if (!alt) {
    throw new Error(`Missing \`alt\` on myImage from: ${src}`);
  }

  if (isDev) {
    return `<img src="${src.slice(3)}" alt="${alt}" />`;
  }

  let stats = await Image(src, {
    widths: [25, 320, 640, 960, 1200, 1800, 2400],
    formats: ['jpeg', 'webp'],
    urlPath: '/images/',
    outputDir: paths.imagesDest,
  });

  let lowestSrc = stats['jpeg'][0];

  const base64Placeholder = await getPlaceHolder(lowestSrc.outputPath);

  const srcset = generateSrcset(stats);

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
};
