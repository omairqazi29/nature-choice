/**
 * Copyright © 2016-present Kriasoft. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

'use strict';

const nodeExternals = require('webpack-node-externals');
const WriteFilePlugin = require('write-file-webpack-plugin');
const paths = require('./paths');

module.exports = function(env) {
  const config = require('./webpack.config')(env, 'node');
  return [
    // Client configuration
    require('./webpack.config')(env),
    // Server configuration
    Object.assign({}, config, {
      name: 'server',
      target: 'node',
      node: false,

      entry: {
        server: paths.appNodeJs,
      },

      output: Object.assign({}, config.output, {
        path: paths.nodeBuild,
        filename: '[name].js',
        libraryTarget: 'commonjs2',
      }),

      optimization: Object.assign({}, config.optimization, {
        minimize: false,
        runtimeChunk: false,
      }),

      plugins: config.plugins.concat([
        new WriteFilePlugin({
          output: paths.nodeBuild,
          test: /^(.(?!hot-update))*$/,
        }),
      ]),

      externals: ['./stats.json', nodeExternals()],
    }),
  ];
};
