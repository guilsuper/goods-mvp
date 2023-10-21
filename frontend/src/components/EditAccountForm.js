/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Button, Form } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import { useEditAccount } from '../api/Account'
import { useUser } from '../lib/Auth'

const EditAccountForm = () => {
  // user is needed to display local storage information
  const user = useUser({})

  // If successfully edited, go to home page to prevent multiple editing
  const navigate = useNavigate()

  const editAccount = useEditAccount()

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const data = {}

    // set data value from the form
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

    editAccount.mutate(data, {
      onSuccess: (data, variables, context) => {
        alert('Successfully edited')
        navigate('/account/info')
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
    <FormContainer>
      <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder={user.data?.email} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter new password" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="first_name">
          <Form.Label>First name</Form.Label>
          <Form.Control type="text" placeholder={user.data?.first_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="last_name">
          <Form.Label>Last name</Form.Label>
          <Form.Control type="text" placeholder={user.data?.last_name} />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditAccountForm
