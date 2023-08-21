/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState } from 'react'
import Form from 'react-bootstrap/Form'
import { useNavigate } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import { Button } from 'react-bootstrap'

const SignUpForm = () => {
  const navigate = useNavigate()

  const [formValues, setFormValues] = useState({
    email: '',
    password: '',
    website: '',
    company_name: '',
    jurisdiction: ''
  })

  const handleChange = (event) => {
    const { id, value } = event.target

    setFormValues((prevState) => ({
      ...prevState,
      [id]: value
    }))
  }

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const formData = new FormData()

    // Add the text data from the state to the FormData
    for (const [key, value] of Object.entries(formValues)) {
      formData.append(key, value)
    }

    const config = {
      method: 'POST',
      body: formData
    }

    let response = ''
    try {
      response = await fetch('/api/admin_and_company/create/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert('Successfully created. Check your email.')
      navigate('/')
    } else if (response.status === 400) {
      let message = 'Invalid input data:'
      for (const invalidElement in result) {
        message += '\n' + invalidElement + ': ' + result[invalidElement]
      }
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
    }
  }

  return (
    <FormContainer>
      <Form onSubmit={submitHandler}>
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

        <Form.Group className="mb-3" controlId="website">
          <Form.Label>Company domain</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter company domain, like example.com"
            value={formValues.website}
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

        <Form.Group className="mb-3" controlId="jurisdiction">
          <Form.Label>Company Jurisdiction of Incorporation</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter company Jurisdiction of Incorporation"
            value={formValues.jurisdiction}
            onChange={handleChange}
          />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Sign Up
        </Button>
      </Form>
    </FormContainer>
  )
}

export default SignUpForm
