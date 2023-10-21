/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import Axios from 'axios'
import { storage } from '../utils/Storage'
import { annotateWithTime, decodeTokens } from '../utils/JWT'

export const axiosNoTokens = Axios.create({
  baseURL: '/api'
})

export const axios = Axios.create({
  baseURL: '/api'
})

function refreshAccessToken () {
  const tokens = storage.getToken()
  if (tokens) {
    const response = axiosNoTokens.post('/token/refresh/', {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      },
      refresh: tokens.refresh
    })
    return response
  }
}

function needNewAccessToken () {
  const tokens = storage.getToken()
  if (tokens) {
    decodeTokens(tokens)

    const localAccessTimeExpiration = tokens.access_decoded.exp - tokens.access_decoded.tdelta

    const now = Date.now() / 1000

    if ((localAccessTimeExpiration - now) < 5 * 60) {
      return true
    } else {
      return false
    }
  }
  return false
}

let refreshingAccessToken = null

const authRequestInterceptor = async (config) => {
  if (needNewAccessToken()) {
    // This ensures only one refreshAccessToken runs at once
    // eslint changed this from ternary operator
    refreshingAccessToken = refreshingAccessToken || refreshAccessToken()
    try {
      const response = await refreshingAccessToken

      if (response.data) {
        const newAuthTokens = response.data
        storage.setToken(annotateWithTime(newAuthTokens))
      }
    } finally {
      refreshingAccessToken = null
    }
  }

  const tokens = storage.getToken()
  if (tokens) {
    config.headers.Authorization = 'Bearer ' + tokens.access
  }
  return config
}

axios.interceptors.request.use(authRequestInterceptor)
