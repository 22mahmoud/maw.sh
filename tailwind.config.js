module.exports = {
  purge: {
    layers: ['utilities', 'components'],
    content: ['web/views/**/**.pug', 'web/js/**/*.ts'],
  },
  theme: {
    extend: {
      fontFamily: {
        display: ['Abril Fatface'],
        sans: ['Merriweather Sans'],
      },
      inset: {
        '1/2': '50%',
      },
    },
  },
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  variants: {},
  plugins: [],
};
