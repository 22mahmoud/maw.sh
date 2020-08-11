module.exports = {
  presets: [
    [
      '@babel/env',
      {
        modules: false,
        useBuiltIns: 'entry',
        corejs: 3.6,
      },
    ],
    '@babel/typescript',
  ],
  plugins: ['@babel/proposal-class-properties'],
};
