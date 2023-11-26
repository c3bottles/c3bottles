const path = require('path');
const webpack = require('webpack');
const nodeEnv = (process.env.NODE_ENV || 'development').trim();
const TerserPlugin = require('terser-webpack-plugin');

// eslint-disable-next-line
const __DEV__ = nodeEnv !== 'production';

const plugins = [
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify(nodeEnv),
    },
  }),
];

const optimization = {
  splitChunks: {
    cacheGroups: {
      commons: {
        name: 'commons',
        chunks: 'initial',
        minChunks: 2,
      },
    },
  },
  minimizer: [],
};

if (!__DEV__) {
  optimization.minimizer.push(
    new TerserPlugin({
      parallel: true,
      extractComments: true,
    })
  );
}

module.exports = {
  mode: __DEV__ ? 'development' : 'production',
  resolve: {
    // Extension die wir weglassen können
    extensions: ['.js', '.jsx'],
    modules: ['node_modules'],
  },
  entry: {
    lib: './js/entries/index.js',
    numbers: './js/entries/numbers.js',
  },
  output: {
    path: path.resolve('static/lib/js'),
    filename: '[name].js',
    publicPath: '/',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader',
      },
      {
        parser: { amd: false },
      },
    ],
  },
  performance: {
    maxAssetSize: 1024000,
    maxEntrypointSize: 1024000
  },
  plugins,
  devtool: __DEV__ ? 'cheap-module-source-map' : 'source-map',
  optimization,
};
