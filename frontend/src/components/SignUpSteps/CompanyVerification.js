/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect } from 'react'
import FormContainer from '../../utils/FormContainer'
import PropTypes from 'prop-types'
import { Button, Form, Col, Row } from 'react-bootstrap'

const CompanyVerification = ({ prevStep, nextStep, setState, state }) => {
  CompanyVerification.propTypes = {
    state: PropTypes.object,
    nextStep: PropTypes.func,
    prevStep: PropTypes.func,
    setState: PropTypes.func
  }
  const [formValues, setFormValues] = useState({
    company_jurisdiction: '',
    company_headquarters_physical_address: ''
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

  const goNext = (event) => {
    event.preventDefault()

    setState((prevState) => ({
      ...prevState,
      ...formValues
    }))

    nextStep()
  }

  const goBack = event => {
    event.preventDefault()

    prevStep()
  }

  return (
    <FormContainer>
      <h2 className="text-center">Company Verification</h2>
      <Form.Group className="mb-3" controlId="company_jurisdiction">
        <Form.Label>Company Jurisdiction of Incorporation</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company Jurisdiction of Incorporation"
          value={formValues.company_jurisdiction}
          onChange={handleChange}
        />
      </Form.Group>
      <Form.Group className="mb-3" controlId="company_headquarters_physical_address">
        <Form.Label>Company Headquarters Physical Address</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter company Headquarters Physical Address"
          value={formValues.company_headquarters_physical_address}
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
          <Button onClick={ goNext } className="mb-3 mx-auto" variant="primary">
            Continue
          </Button>
        </Col>
      </Row>
    </FormContainer>
  )
}

export default CompanyVerification
