/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { configureAuth } from 'react-query-auth'

import { signInUser, getUser, getUserWTokens } from '../api/Account'

import { storage } from '../utils/Storage'
import { annotateWithTime } from '../utils/JWT'

async function userFn () {
  if (storage.getToken() == null) return null
  else {
    const user = await getUser()
    return user ?? null
  }
}

async function loginFn (data) {
  const tokens = await signInUser(data)
  const user = await getUserWTokens(tokens)
  storage.setToken(annotateWithTime(tokens))
  return user
}

async function logoutFn () {
  storage.clearToken()
}

export const { useUser, useLogin, useLogout, AuthLoader } =
  configureAuth({
    userFn,
    loginFn,
    logoutFn
  })
