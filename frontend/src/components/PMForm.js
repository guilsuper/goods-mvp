/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext } from 'react'
import { Button, Form } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

const PMForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  const { authTokens } = useContext(AuthContext)
  // If successfully editted, go to account/pm to prevent multiple editting
  const navigate = useNavigate()

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()
    const data = {}

    Object.keys(event.target).forEach(function (attr) {
      if (!isNaN(attr)) {
        if (event.target[attr].style) {
          // Clear bg color
          event.target[attr].style = ''
        }
        if (event.target[attr].value !== '') {
          // Add key and value pair to data from form field
          data[event.target[attr].id] = event.target[attr].value
        }
      }
    })

    // Config for POST request
    const config = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      },
      body: JSON.stringify(data)
    }

    let response = ''
    try {
      response = await fetch('/api/pm/create/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert('Successfully created')
      navigate('/account/pm')
    } else if (response.status === 400) {
      let message = 'Invalid input data:'
      for (const invalidElement in result) {
        event.target[invalidElement].style = 'border-color: red'

        message += '\n' + invalidElement + ': ' + result[invalidElement]
      }
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
    }
  }

  return (
    <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="email">
        <Form.Label>Email</Form.Label>
        <Form.Control type="email" placeholder="Enter email" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="password">
        <Form.Label>Password</Form.Label>
        <Form.Control type="password" placeholder="Enter password" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="first_name">
        <Form.Label>First name</Form.Label>
        <Form.Control type="text" placeholder="Enter first name" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="last_name">
        <Form.Label>Last name</Form.Label>
        <Form.Control type="text" placeholder="Enter last name" />
      </Form.Group>

      <Button className="mb-3" variant="primary" type="submit">
        Create PM
      </Button>
    </Form>
  )
}

export default PMForm
