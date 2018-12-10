module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        loose: false,
        useBuiltIns: 'entry',
      },
      'babel-preset-joblift',
    ],
  ],
};
