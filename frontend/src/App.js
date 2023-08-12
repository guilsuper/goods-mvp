/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import {
  BrowserRouter as Router, Routes, Route
} from "react-router-dom";
import React from "react";

import "./App.css";
import Header from "./components/Header";
import ProductList from "./pages/ProductList";
import Home from "./pages/Home";
import SignUp from "./pages/SignUp";
import SignIn from "./pages/SignIn";
import Footer from "./components/Footer";
import PrivateRoute from "./utils/PrivateRoute";
import AccountInfo from "./pages/AccountInfo";
import { AuthProvider } from "./context/AuthContext";
import EditAccountForm from "./components/EditAccountForm";
import ActivatePage from "./pages/ActivatePage";
import CompanyProducts from "./pages/CompanyProducts";
import CompanyPM from "./pages/CompanyPM";
import PMAccountInfo from "./pages/PMAccountInfo";
import ProductInfo from "./pages/ProductInfo";
import EditPMForm from "./components/EditPMForm";
import EditProductForm from "./components/EditProductForm";


function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="d-flex flex-column min-vh-100">
          <Header/>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<ProductList />} />
            <Route path="/products/:product_sku" element={<ProductInfo />} />
            <Route path="/sign-up" element={<SignUp />} />
            <Route path="/sign-in" element={<SignIn />} />
            <Route path="/activated/:uidb64/:token" element={<ActivatePage />} />
            <Route exact path="/account" element={<PrivateRoute/>}>
              <Route exact path="/account/info" element={<AccountInfo />}/>
              <Route exact path="/account/products" element={<CompanyProducts />}/>
              <Route exact path="/account/products/edit/:product_sku" element={<EditProductForm />}/>
              <Route exact path="/account/edit" element={<EditAccountForm />}/>
              <Route exact path="/account/pm" element={<CompanyPM />}/>
              <Route exact path="/account/pm/edit/:pm_email" element={<EditPMForm />}/>
              <Route exact path="/account/pm/info/:pm_email" element={<PMAccountInfo />}/>
            </Route>
          </Routes>
          <Footer />
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App
