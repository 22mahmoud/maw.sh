module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    project: [
      './tsconfig.json',
      './tsconfig.tooling.json',
      './tsconfig.web.json',
    ],
  },
  extends: [
    'airbnb-typescript/base',
    'prettier/@typescript-eslint',
    'plugin:prettier/recommended',
  ],
  rules: {
    'import/prefer-default-export': 'off',
    'import/no-default-export': 'error',
    '@typescript-eslint/no-empty-interface': 'off',
  },
};
