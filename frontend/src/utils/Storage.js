/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

export const storage = {
  getToken: () => JSON.parse(window.localStorage.getItem('authTokens') || 'null'),
  setToken: (token) =>
    window.localStorage.setItem('authTokens', JSON.stringify(token)),
  clearToken: () => window.localStorage.removeItem('authTokens')
}
