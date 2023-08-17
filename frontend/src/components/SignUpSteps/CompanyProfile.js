/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import FormContainer from '../../utils/FormContainer'
import { Button, Form, Col, Row } from 'react-bootstrap'

const CompanyProfile = ({ prevStep, setState, state }) => {
  CompanyProfile.propTypes = {
    state: PropTypes.object,
    prevStep: PropTypes.func,
    setState: PropTypes.func
  }

  const [formValues, setFormValues] = useState({
    industry: '',
    company_size: '',
    company_phonenumber: ''
  })

  useEffect(() => {
    setFormValues((prevState) => ({
      ...prevState,
      ...state
    }))
  }, [setFormValues, state])

  const handleChange = (event) => {
    const { id, value } = event.target
    setState((prevState) => ({
      ...prevState,
      [id]: value
    }))
    setFormValues((prevState) => ({
      ...prevState,
      [id]: value
    }))
  }

  const goBack = event => {
    event.preventDefault()

    prevStep()
  }

  return (
    <FormContainer>
      <h2 className="text-center">Optional fields</h2>
      <Form.Group className="mb-3" controlId="industry">
        <Form.Group className="mb-3" controlId="first_name">
            <Form.Label>First name</Form.Label>
            <Form.Control
            type="text"
            placeholder="Enter first name"
            value={formValues.first_name}
            onChange={handleChange}
            />
        </Form.Group>
        <Form.Group className="mb-3" controlId="last_name">
            <Form.Label>Last name</Form.Label>
            <Form.Control
            type="text"
            placeholder="Enter last name"
            value={formValues.last_name}
            onChange={handleChange}
            />
        </Form.Group>
        <Form.Group className="mb-3" controlId="phonenumber">
            <Form.Label>Phone</Form.Label>
            <Form.Control
            type="text"
            placeholder="Enter phone"
            value={formValues.phonenumber}
            onChange={handleChange}
            />
        </Form.Group>
        <Form.Label>Industry</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter an industry"
          value={formValues.industry}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="company_size">
        <Form.Label>Company size</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company size"
          value={formValues.company_size}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="company_phonenumber">
        <Form.Label>Company phonenumber</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter Company phonenumber"
          value={formValues.company_phonenumber}
          onChange={handleChange}
        />
      </Form.Group>

      <Row className="justify-content-md-center">
        <Col md={2}>
          <Button onClick={ goBack } className="mb-3" variant="secondary">
            Return
          </Button>
        </Col>
        <Col>
          <Button className="mb-3" variant="primary" type="submit">
            Sign Up
          </Button>
        </Col>
      </Row>
    </FormContainer>
  )
}

export default CompanyProfile
