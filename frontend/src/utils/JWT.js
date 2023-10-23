/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import jwtDecode from 'jwt-decode'

export function annotateWithTime (tokens) {
  const lat = Date.now() / 1000
  tokens.lat = lat
  return tokens
}

export function decodeTokens (tokens) {
  tokens.access_decoded = jwtDecode(tokens.access)
  tokens.access_decoded.tdelta = tokens.access_decoded.iat - tokens.lat

  tokens.refresh_decoded = jwtDecode(tokens.refresh)
  tokens.refresh_decoded.tdelta = tokens.refresh_decoded.iat - tokens.lat

  return tokens
}
