/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import FormContainer from "../utils/FormContainer";
import { useNavigate } from "react-router-dom";


const SignUpForm = () => {

  let navigate = useNavigate()

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    let data = {}

    // set data value from the form
    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        if (event.target[attr].style){
            // Clear bg color
            event.target[attr].style = ""
        }
        if (event.target[attr].value !== ""){
            // Add key and value pair to data from form field
            data[event.target[attr].id] = event.target[attr].value
        }
      }
    })

    const config = {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    }

    let response = ""
    try {
      response = await fetch("/api/admin/create/", config)
    }
    catch (error) {
      alert("Server is not working")
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert("Successfully created. Check your email.")
      navigate("/")
    }
    else if (response.status === 400) {
      let message = "Invalid input data:"
      for (const invalid_element in result){
        event.target[invalid_element].style = "border-color: red"

        message += "\n" + invalid_element + ": " + result[invalid_element]
      }
      alert(message)
    }
    else {
      alert("Not authenticated or permission denied")
    }
  }

  return (
    <FormContainer>
      <Form onSubmit={submitHandler}>
        <Form.Group className="mb-3" controlId="username">
          <Form.Label>Username</Form.Label>
          <Form.Control type="text" placeholder="Enter username" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter password" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_name">
          <Form.Label>Company name</Form.Label>
          <Form.Control type="text" placeholder="Enter company name" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_address">
          <Form.Label>Company address</Form.Label>
          <Form.Control type="text" placeholder="Enter company address" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="industry">
          <Form.Label>Industry</Form.Label>
          <Form.Control type="text" placeholder="Enter an industry" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_size">
          <Form.Label>Company size</Form.Label>
          <Form.Control type="text" placeholder="Enter company size" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="first_name">
          <Form.Label>First name</Form.Label>
          <Form.Control type="text" placeholder="Enter first name" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="last_name">
          <Form.Label>Last name</Form.Label>
          <Form.Control type="text" placeholder="Enter last name" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder="Enter email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="phonenumber">
          <Form.Label>Phone</Form.Label>
          <Form.Control type="text" placeholder="Enter phone" />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Sign Up
        </Button>
      </Form>
    </FormContainer>
  )
}

export default SignUpForm
