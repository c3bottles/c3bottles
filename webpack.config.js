const path = require('path');
const webpack = require('webpack');
const nodeEnv = (process.env.NODE_ENV || 'development').trim();

// eslint-disable-next-line
const __DEV__ = nodeEnv !== 'production';

const devtool = __DEV__ ? '#source-map' : '';

const plugins = [
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify(nodeEnv),
    },
  }),
];

if (!__DEV__) {
  plugins.push(
    new webpack.optimize.UglifyJsPlugin({
      compress: {
        warnings: false,
      },
      output: {
        comments: false,
      },
      screwIe8: true,
      sourceMap: false,
    })
  );
}

module.exports = {
  context: __dirname,
  resolve: {
    // Extension die wir weglassen können
    extensions: ['.js', '.jsx'],
    modules: ['node_modules'],
  },
  entry: ['babel-polyfill', './js/index.js'],
  output: {
    path: path.resolve('static/lib/js'),
    filename: 'lib.js',
    publicPath: '/',
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
      },
      {
        parser: { amd: false },
      }
    ],
  },
  plugins,
  devtool,
};
