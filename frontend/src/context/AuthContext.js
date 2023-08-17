/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { createContext, useState } from 'react'
import PropTypes from 'prop-types'
import { useNavigate } from 'react-router-dom'

const AuthContext = createContext()

export default AuthContext

export const AuthProvider = (props) => {
  AuthProvider.propTypes = {
    children: PropTypes.any
  }

  const children = props.children

  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
  )
  const [user, setUser] = useState(() =>
    localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null
  )

  const navigate = useNavigate()

  const updateUser = async () => {
    const config = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/self/patch_delete_retrieve/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }
    const data = await response.json()

    localStorage.setItem('user', JSON.stringify(data))
    setUser(data)
  }

  const signInUser = async (event, tokens) => {
    const config = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + tokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/self/patch_delete_retrieve/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }
    const data = await response.json()

    localStorage.setItem('authTokens', JSON.stringify(tokens))
    localStorage.setItem('user', JSON.stringify(data))

    setAuthTokens(tokens)
    setUser(data)

    navigate('/account/info')
  }

  const logoutUser = () => {
    localStorage.removeItem('authTokens')
    localStorage.removeItem('user')

    setAuthTokens(null)
    setUser(null)

    navigate('/sign-in')
  }

  const contextData = {
    user,
    authTokens,
    signInUser,
    updateUser,
    logoutUser
  }

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  )
}
