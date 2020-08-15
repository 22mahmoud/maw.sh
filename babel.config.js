module.exports = (api) => {
  api.cache.using(() => process.env.NODE_ENV);

  const isTargetWeb = api.caller((caller) => caller && caller.target === 'web');

  // const isDev = ['test', 'production'].includes(process.env.NODE_ENV) === false;

  return {
    presets: [
      [
        '@babel/env',
        {
          modules: false,
          useBuiltIns: 'entry',
          corejs: 3.6,
          ...(!isTargetWeb && {
            targets: {
              node: 'current',
            },
          }),
        },
      ],
      '@babel/typescript',
    ],
    plugins: ['@babel/proposal-class-properties'],
  };
};
