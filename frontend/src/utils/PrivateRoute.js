/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { storage } from '../utils/Storage'

const PrivateRoute = () => {
  const authTokens = storage.getToken()

  return authTokens ? <Outlet /> : <Navigate to="/" />
}

export default PrivateRoute
