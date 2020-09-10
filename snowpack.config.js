module.exports = {
  install: ['vanilla-lazyload'],
  mount: {
    site: '/',
    'src/styles': '/styles',
    'src/js': '/js',
  },

  plugins: [
    '@snowpack/plugin-postcss',
    ['@snowpack/plugin-run-script', { cmd: 'eleventy', watch: '$1 --watch' }],
  ],

  devOptions: {
    port: 3000,
    open: 'none',
    hmr: true,
  },
};
