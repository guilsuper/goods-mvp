/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState, useEffect } from 'react'
import { Button, Form } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'

const EditPMForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  const { authTokens } = useContext(AuthContext)
  const { pmEmail } = useParams()
  const [pm, setPM] = useState([])
  // If successfully edited, go to home page to prevent multiple editing
  const navigate = useNavigate()

  useEffect(() => {
    async function getPMInfo () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + authTokens.access
        }
      }

      let response = ''
      try {
        response = await fetch('/api/pm/patch_delete_retrieve/' + pmEmail + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        setPM(result)
      }
    }
    getPMInfo()
  }, [authTokens, navigate, pmEmail])

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

    // Config for PATCH request
    const config = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      },
      body: JSON.stringify(data)
    }

    let response = ''
    try {
      response = await fetch('/api/pm/patch_delete_retrieve/' + pmEmail + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    const result = await response.json()

    if (response.status === 200) {
      alert('Successfully edited')
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
    <FormContainer>
      <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="email">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" placeholder={pm.email} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="first_name">
            <Form.Label>First name</Form.Label>
            <Form.Control type="text" placeholder={pm.first_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="last_name">
            <Form.Label>Last name</Form.Label>
            <Form.Control type="text" placeholder={pm.last_name} />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
            Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditPMForm
