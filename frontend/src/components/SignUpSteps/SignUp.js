/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect } from "react";
import FormContainer from "../../utils/FormContainer";
import { Button, Form } from "react-bootstrap";


const SignUp = ({ nextStep, setState, state }) => {

  const [formValues, setFormValues] = useState({
    company_administrator_email: "",
    password: "",
    company_website: "",
    company_name: ""
  });

  useEffect(() => {
    setFormValues((prevState) => ({
      ...prevState,
      ...state
    }))
  }, [setFormValues, state])

  const handleChange = (event) => {
    const { id, value } = event.target;
    setState((prevState) => ({
      ...prevState,
      [id]: value
    }))
    setFormValues((prevState) => ({
      ...prevState,
      [id]: value
    }))
  }

  const goNext = (event) => {
    event.preventDefault();

    nextStep();
  }

  return (
    <FormContainer>
      <h2 className="text-center">Sign Up</h2>
      <Form.Group className="mb-3" controlId="email">
        <Form.Label>Company Administrator Email Address</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company administrator email"
          value={formValues.email}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="password">
        <Form.Label>Password</Form.Label>
        <Form.Control
          type="password"
          placeholder="Enter password"
          value={formValues.password}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="company_website">
        <Form.Label>Company domain</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company domain, like example.com"
          value={formValues.company_website}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="company_name">
        <Form.Label>Company legal name</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company legal name"
          value={formValues.company_name}
          onChange={handleChange}
        />
      </Form.Group>

      <Button onClick={ goNext } className="mb-3 mx-auto" variant="primary">
        Continue
      </Button>
    </FormContainer>
  )
}

export default SignUp
