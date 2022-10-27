// const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  optimization: {
    minimize: false,
  },
  entry: {
    app: './src/index.js',
    examples: './src/examples/index.js',
  },
  module: {
    rules: [
      { test: /\.yaml$/, use: 'yaml-loader' },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html',
      filename: 'index.html',
      chunks: ['app'],
    }),
    new HtmlWebpackPlugin({
      template: './examples.html',
      filename: 'examples.html',
      chunks: ['examples'],
    }),
  ],
};
