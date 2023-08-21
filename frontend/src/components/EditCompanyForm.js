/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext } from 'react'
import { Button, Form } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useParams, useNavigate } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'

const EditCompanyForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  const { authTokens, updateUser, user } = useContext(AuthContext)
  // If successfully editted, go to home page to prevent multiple editting
  const navigate = useNavigate()

  const { companyName } = useParams()

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
      response = await fetch('/api/company/patch_retrieve/' + companyName + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    const result = await response.json()

    if (response.status === 200) {
      alert('Successfully editted')
      updateUser()
      navigate('/account/info')
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
        <Form.Group className="mb-3" controlId="company_name">
          <Form.Label>Company name</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_website">
          <Form.Label>Company website</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_website} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_jurisdiction">
          <Form.Label>Company jurisdiction</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_jurisdiction} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_headquarters_physical_address">
          <Form.Label>Company headquarters physical address</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_headquarters_physical_address} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="industry">
          <Form.Label>Industry</Form.Label>
          <Form.Control type="text" placeholder={user.company.industry} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_size">
          <Form.Label>Company size</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_size} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="company_phonenumber">
          <Form.Label>Company phonenumber</Form.Label>
          <Form.Control type="text" placeholder={user.company.company_phonenumber} />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditCompanyForm
