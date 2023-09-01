/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import {
  BrowserRouter as Router, Routes, Route
} from 'react-router-dom'
import React from 'react'

import './App.css'
import Header from './components/Header'
import SCTRList from './pages/SCTRList'
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
import CompanySCTR from './pages/CompanySCTR'
import CompanyPM from './pages/CompanyPM'
import PMAccountInfo from './pages/PMAccountInfo'
import SCTRInfo from './pages/SCTRInfo'
import EditPMForm from './components/EditPMForm'
import EditSCTRForm from './components/EditSCTRForm'
import CompanyInfo from './pages/CompanyInfo'
import EditCompanyForm from './components/EditCompanyForm'
import SCTRCreate from './pages/SCTRCreate'

function App () {
  return (
    <Router>
      <AuthProvider>
        <div className="d-flex flex-column min-vh-100">
          <Header/>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sctr" element={<SCTRList />} />
            <Route path="/sctr/:sctrIdentifier" element={<SCTRInfo />} />
            <Route path="/about" element={<About />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/activated/:uidb64/:token" element={<ActivatePage />} />
            <Route exact path="/account" element={<PrivateRoute/>}>
              <Route exact path="/account/info" element={<AccountInfo />}/>
              <Route exact path="/account/sctr" element={<CompanySCTR />}/>
              <Route exact path="/account/sctr/create" element={<SCTRCreate />}/>
              <Route exact path="/account/sctr/edit/:sctrIdentifier" element={<EditSCTRForm />}/>
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
