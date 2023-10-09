/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState, useEffect } from 'react'
import { Button, Form } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useParams, useNavigate } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import CompanyLogo from './CompanyLogo'

const EditCompanyForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  const { authTokens, updateUser } = useContext(AuthContext)
  // If successfully edited, go to home page to prevent multiple editing
  const navigate = useNavigate()

  const { companyName } = useParams()
  const [company, setCompany] = useState([])

  useEffect(() => {
    async function getCompanyInfo () {
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
        response = await fetch('/api/company/patch_retrieve/' + companyName + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      let result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        result = { ...result, ...result.company }
        delete result.company
        setCompany(result)
      }
    }
    getCompanyInfo()
  }, [navigate, companyName, authTokens.access])

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const data = new FormData()

    // Handle the file input
    if (event.target.logo.files.length !== 0) {
      data.append('logo', event.target.logo.files[0])
    }

    // Append data if was set in the form
    const fields = ['name', 'website', 'jurisdiction']
    fields.map(
      field => event.target[field].value ? data.append(field, event.target[field].value) : company[field]
    )

    // Config for PATCH request
    const config = {
      method: 'PATCH',
      headers: {
        Authorization: 'Bearer ' + authTokens.access
      },
      body: data
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
      alert('Successfully edited')
      updateUser()
      navigate('/account/info')
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
        <Form.Group className="mb-3" controlId="name">
          <Form.Label>Company name</Form.Label>
          <Form.Control type="text" placeholder={company.name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="website">
          <Form.Label>Company website</Form.Label>
          <Form.Control type="text" placeholder={company.website} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="jurisdiction">
          <Form.Label>Company jurisdiction</Form.Label>
          <Form.Control type="text" placeholder={company.jurisdiction} />
        </Form.Group>

        {
          // If logo is set
          company.logo
            ? <CompanyLogo companyLogo={company.logo} />
            : ' '
        }

        <Form.Group controlId="logo" className="mb-3">
          <Form.Label>Update company logo</Form.Label>
          <Form.Control type="file" />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditCompanyForm
