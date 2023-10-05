/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import {
  BrowserRouter as Router, Routes, Route
} from 'react-router-dom'
import React from 'react'

import './App.css'
import Header from './components/Header'
import OriginReportList from './pages/OriginReportList'
import Home from './pages/Home'
import OurMission from './pages/OurMission'
import Terms from './pages/Terms'
import SignUp from './pages/SignUp'
import SignIn from './pages/SignIn'
import Footer from './components/Footer'
import PrivateRoute from './utils/PrivateRoute'
import AccountInfo from './pages/AccountInfo'
import { AuthProvider } from './context/AuthContext'
import EditAccountForm from './components/EditAccountForm'
import ActivatePage from './pages/ActivatePage'
import CompanyOriginReport from './pages/CompanyOriginReport'
import CompanyPM from './pages/CompanyPM'
import PMAccountInfo from './pages/PMAccountInfo'
import OriginReportInfo from './pages/OriginReportInfo'
import EditPMForm from './components/EditPMForm'
import EditOriginReportForm from './components/EditOriginReportForm'
import CompanyInfo from './pages/CompanyInfo'
import EditCompanyForm from './components/EditCompanyForm'
import OriginReportCreate from './pages/OriginReportCreate'

function App () {
  return (
    <Router>
      <AuthProvider>
        <div className="d-flex flex-column min-vh-100">
          <Header/>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/origin_report" element={<OriginReportList />} />
            <Route path="/origin_report/:originReportIdentifier" element={<OriginReportInfo />} />
            <Route path="/our_mission" element={<OurMission />} />
            <Route path="/terms" element={<Terms />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/activated/:uidb64/:token" element={<ActivatePage />} />
            <Route exact path="/account" element={<PrivateRoute/>}>
              <Route exact path="/account/info" element={<AccountInfo />}/>
              <Route exact path="/account/origin_report" element={<CompanyOriginReport />}/>
              <Route exact path="/account/origin_report/create" element={<OriginReportCreate />}/>
              <Route exact path="/account/origin_report/edit/:originReportIdentifier" element={<EditOriginReportForm />}/>
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
