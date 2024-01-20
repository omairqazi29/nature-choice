'use strict';

const fs = require('fs');
const paths = require('./paths');

module.exports = function(env) {
  return fs.existsSync(paths.webpackConfig)
    ? require(paths.webpackConfig)(env)
    : require('./webpack')(env);
};
