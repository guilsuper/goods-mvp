/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

/*
 * Contents derived from examples found online:
 *   - https://scoutapm.com/blog/how-to-use-docker-healthcheck
 *   - https://anthonymineo.com/docker-healthcheck-for-your-node-js-app
 */

const http = require('http')

const options = {
  host: 'localhost',
  port: '3000',
  timeout: 2000
}

const request = http.request(options, (res) => {
  console.log(`HEALTHCHECK STATUS: ${res.statusCode}`)
  if (res.statusCode === 200) {
    process.exit(0)
  } else {
    process.exit(1)
  }
})

request.on('error', function (err) {
  console.log('ERROR')
  console.log(err)
  process.exit(1)
})
request.end()
