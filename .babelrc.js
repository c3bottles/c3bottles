module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        corejs: 3,
        loose: false,
        useBuiltIns: 'usage',
      },
    ],
  ],
};
