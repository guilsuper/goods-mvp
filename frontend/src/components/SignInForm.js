/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { useNavigate } from 'react-router-dom'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormContainer from '../utils/FormContainer'
import { useLogin } from '../lib/Auth'

const SignIn = () => {
  const navigate = useNavigate()

  const login = useLogin()

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const data = {}

    // set data value from the form
    Object.keys(event.target).forEach(function (attr) {
      if (!isNaN(attr)) {
        data[event.target[attr].id] = event.target[attr].value
      }
    })

    login.mutate({ data }, {
      onSuccess: (data, variables, context) => {
        alert('Successfully logged')
        navigate('/account/info')
      },
      onError: (error, variables, context) => {
        if (error.request?.status === 401) {
          alert('Invalid input data')
        } else {
          alert('Not authenticated or permission denied')
        }
      }
    })
  }

  return (
    <FormContainer>
      <Form onSubmit={submitHandler}>
        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="text" placeholder="Enter email" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter password" />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Sign In
        </Button>
      </Form>
    </FormContainer>
  )
}

export default SignIn
