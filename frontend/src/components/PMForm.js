/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Button, Form } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import { useCreateProductManager } from '../api/ProductManager'

const PMForm = () => {
  // If successfully edited, go to account/pm to prevent multiple editing
  const navigate = useNavigate()

  const createProductManager = useCreateProductManager()

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

    createProductManager.mutate(data, {
      onSuccess: (data, variables, context) => {
        alert('Successfully created')
        navigate('/account/pm')
      },
      onError: (error, variables, context) => {
        if (error.request?.status === 400) {
          let message = 'Invalid input data:'
          for (const invalidElement in error.response.data) {
            event.target[invalidElement].style = 'border-color: red'
            message += '\n' + invalidElement + ': ' + error.response.data[invalidElement]
          }
          alert(message)
        } else {
          alert('Not authenticated or permission denied')
        }
      }
    })
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
