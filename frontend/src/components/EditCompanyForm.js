/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Button, Form } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import ImageComponent from './ImageComponent'
import { useGetCompanyQuery, useEditCompany } from '../api/Company'
import LoadingComponent from './LoadingComponent'

const EditCompanyForm = () => {
  const navigate = useNavigate()

  const { companyName } = useParams()

  const { isLoading, isError, data: company, error } = useGetCompanyQuery({ name: companyName })

  const editCompany = useEditCompany()

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

    editCompany.mutate({ name: companyName, update: data }, {
      onSuccess: (data, variables, context) => {
        alert('Successfully edited')
        navigate('/account/info')
      },
      onError: (error, variables, context) => {
        if (error.request?.status === 400) {
          let message = 'Invalid input data:'
          for (const invalidElement in error.response.data) {
            message += '\n' + invalidElement + ': ' + error.response.data[invalidElement]
          }
          alert(message)
        } else {
          alert('Not authenticated or permission denied')
        }
      }
    })
  }

  if (isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (isError) {
    return (
      <h2 className="text-center">An error has occurred: { error.message }</h2>
    )
  } else {
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
              ? <ImageComponent src={company.logo} text={'Company logo'}/>
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
}

export default EditCompanyForm
