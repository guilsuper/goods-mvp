/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import {
  BrowserRouter as Router, Routes, Route
} from 'react-router-dom'
import React from 'react'

import './App.css'
import Header from './components/Header'
import ProductList from './pages/ProductList'
import Home from './pages/Home'
import About from './pages/About'
import Terms from './pages/Terms'
import SignUp from './pages/SignUp'
import SignIn from './pages/SignIn'
import Footer from './components/Footer'
import PrivateRoute from './utils/PrivateRoute'
import AccountInfo from './pages/AccountInfo'
import { AuthProvider } from './context/AuthContext'
import EditAccountForm from './components/EditAccountForm'
import ActivatePage from './pages/ActivatePage'
import CompanyProducts from './pages/CompanyProducts'
import CompanyPM from './pages/CompanyPM'
import PMAccountInfo from './pages/PMAccountInfo'
import ProductInfo from './pages/ProductInfo'
import EditPMForm from './components/EditPMForm'
import EditProductForm from './components/EditProductForm'
import CompanyInfo from './pages/CompanyInfo'
import EditCompanyForm from './components/EditCompanyForm'

function App () {
  return (
    <Router>
      <AuthProvider>
        <div className="d-flex flex-column min-vh-100">
          <Header/>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<ProductList />} />
            <Route path="/products/:productSku" element={<ProductInfo />} />
            <Route path="/about" element={<About />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/activated/:uidb64/:token" element={<ActivatePage />} />
            <Route exact path="/account" element={<PrivateRoute/>}>
              <Route exact path="/account/info" element={<AccountInfo />}/>
              <Route exact path="/account/products" element={<CompanyProducts />}/>
              <Route exact path="/account/products/edit/:productSku" element={<EditProductForm />}/>
              <Route exact path="/account/edit" element={<EditAccountForm />}/>
              <Route exact path="/account/pm" element={<CompanyPM />}/>
              <Route exact path="/account/pm/edit/:pmEmail" element={<EditPMForm />}/>
              <Route exact path="/account/pm/info/:pmEmail" element={<PMAccountInfo />}/>
              <Route exact path="/account/company/info/:companyName" element={<CompanyInfo />}/>
              <Route exact path="/account/company/edit/:companyName" element={<EditCompanyForm />}/>
            </Route>
          </Routes>
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
