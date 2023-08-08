import React, { useState, useEffect } from "react";
import FormContainer from "../../utils/FormContainer";
import { Button, Form } from "react-bootstrap";


const SignUp = ({ nextStep, setState, state, handleSubmit }) => {

  const [formValues, setFormValues] = useState({
    email: "",
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

  const updateStateSubmit = (event) => {
    event.preventDefault();

    handleSubmit(event)
  }

  return (
    <FormContainer>
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
        <Form.Label>Company website</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company website"
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

      <Button onClick={ updateStateSubmit } className="mb-3 mx-auto" variant="primary">
        Sign Up
      </Button>
    </FormContainer>
  )
}

export default SignUp
