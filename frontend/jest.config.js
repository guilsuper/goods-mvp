/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

module.exports = {
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: '../test-results/',
      outputName: 'jest.xml'
    }]
  ]
}
