module.exports = {
  mount: {
    site: '/',
    'src/styles': '/styles',
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
