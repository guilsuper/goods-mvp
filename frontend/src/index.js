/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

import './i18n'

import '../node_modules/bootstrap/dist/css/bootstrap.min.css'

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <React.Suspense fallback="loading">
      <App />
    </React.Suspense>
  </React.StrictMode>
)
