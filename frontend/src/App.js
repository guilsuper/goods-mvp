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
import ProductForm from "./components/ProductForm";
import EditAccountForm from "./components/EditAccountForm";
import ActivatePage from "./components/ActivatePage";


function App() {
  return (
      <Router>
        <AuthProvider>
          <div className="d-flex flex-column min-vh-100">
            <Header/>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/products" element={<ProductList />} />
                <Route path="/sign-up" element={<SignUp />} />
                <Route path="/sign-in" element={<SignIn />} />
                <Route path="/activated/:uidb64/:token" element={<ActivatePage />} />
                <Route exact path="/account" element={<PrivateRoute/>}>
                  <Route exact path="/account/info" element={<AccountInfo />}/>
                  <Route exact path="/account/create_product" element={<ProductForm />}/>
                  <Route exact path="/account/edit" element={<EditAccountForm />}/>
                </Route>
            </Routes>
            <Footer />
          </div>
        </AuthProvider>
      </Router>
  );
}

export default App;
