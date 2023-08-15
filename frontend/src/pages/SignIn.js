/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from "react";
import Container from "react-bootstrap/Container";
import SignInForm from "../components/SignInForm";


const SignIn = () => {
  return (
    <Container>
        <h3 className="text-center">Search for Products Made in the Free World</h3>
        <SignInForm />
    </Container>
  )
}

export default SignIn
