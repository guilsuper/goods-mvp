/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState, useMemo, useEffect } from 'react'
import { Button, Form, Container, Row, Col } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router'
import countryList from 'react-select-country-list'
import { Typeahead } from 'react-bootstrap-typeahead'

const SCTRForm = () => {
  // authTokens are for sending request to the backend
  const { authTokens } = useContext(AuthContext)
  // all possible countries list
  const options = useMemo(() => countryList().getData(), [])
  const [inputFields, setInputFields] = useState([{
    fraction_cogs: 0,
    marketing_name: '',
    component_type_str: 'EXTERNALLY_SOURCED',
    external_sku: '',
    country_of_origin: ''
  }])
  // For different submits
  const [submitButton, setSubmitButton] = useState([{
    button: ''
  }])
  const [sctrs, setSCTRs] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getSCTRs () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      }
      let response = ''
      try {
        response = await fetch('/api/sctr/get/', config)
      } catch (error) {
        alert('Server is not responding')
        return
      }
      const data = await response.json()

      if (response.status === 200) {
        setSCTRs(data)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
    getSCTRs()
  }, [setSCTRs])

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    // set data value from the form
    const data = {
      unique_identifier:
        event.target.unique_identifier.value,

      unique_identifier_type_str:
        event.target.unique_identifier_type_str.value,

      marketing_name:
        event.target.marketing_name[0].value
    }

    data.components = inputFields

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
      if (submitButton === 'draft') {
        response = await fetch('/api/sctr/create_draft/', config)
      } else {
        response = await fetch('/api/sctr/create/', config)
      }
    } catch (error) {
      alert('Server is not working')
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert('Successfully created')
      navigate('/account/sctr')
    } else if (response.status === 400) {
      let message = 'Invalid input data:'
      for (const invalidElement in result) {
        if (invalidElement === 'components') {
          if (Array.isArray(result.components)) {
            for (const index in result.components) {
              for (const field in result.components[index]) {
                message += '\n' + invalidElement + ' ' + (+index + 1) + ': ' + field + ' ' + result.components[index][field]
              }
            }
          } else {
            message += '\n' + invalidElement + ': ' + result[invalidElement]
          }
        } else {
          message += '\n' + invalidElement + ': ' + result[invalidElement]
        }
      }
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
    }
  }

  const handleAddFields = () => {
    const values = [...inputFields]
    values.push({
      fraction_cogs: 0,
      marketing_name: '',
      component_type_str: 'EXTERNALLY_SOURCED',
      external_sku: '',
      country_of_origin: ''
    })
    setInputFields(values)
  }

  const handleRemoveFields = index => {
    const values = [...inputFields]
    values.splice(index, 1)
    setInputFields(values)
  }

  const handleInputChange = (index, event) => {
    const values = [...inputFields]
    values[index][event.target.id] = event.target.value

    setInputFields(values)
  }

  const handleExternalSKUChange = (index, text, event) => {
    // event here doesn't have event.target.id
    const values = [...inputFields]
    values[index].external_sku = text

    setInputFields(values)
  }

  const calculateCOGS = () => {
    const sum = inputFields.reduce(function (prev, current) {
      return prev + +current.fraction_cogs
    }, 0)
    // If NaN
    if (!sum) {
      return 0
    }
    return sum
  }

  return (
    <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="unique_identifier">
        <Form.Label>Identifier</Form.Label>
        <Form.Control type="text" placeholder="Enter unique identifier" />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Identifier type</Form.Label>
        <Form.Select aria-label="Select type" id="unique_identifier_type_str">
          <option value="SKU">SKU</option>
          <option value="GNIT">GNIT</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="marketing_name">
        <Form.Label>Marketing name</Form.Label>
        <Form.Control type="text" placeholder="Enter marketing name" />
      </Form.Group>

      <p>COGS: {calculateCOGS()}%</p>

      <Row>
        <Col className='ps-4'>
          <p>Fraction COGS</p>
        </Col>
        <Col className='ps-4'>
          <p>Marketing name</p>
        </Col>
        <Col className='ps-4'>
          <p>Component type</p>
        </Col>
        <Col className='ps-4'>
          <p>External SKU and Country of Origin</p>
        </Col>
      </Row>

      {inputFields.map((inputField, index) => (
        <Row key={`${inputField}~${index}`} className='mb-3 p-3 border rounded'>
          <Col>
            <Form.Group className="mb-3" controlId="fraction_cogs">
              <Form.Control
                type="text"
                placeholder="Enter fraction COGS"
                value={inputField.fraction_cogs}
                onChange={event => handleInputChange(index, event)}
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group className="mb-3" controlId="marketing_name">
              <Form.Control
                type="text"
                placeholder="Enter marketing name"
                value={inputField.marketing_name}
                onChange={event => handleInputChange(index, event)}
              />
            </Form.Group>
          </Col>
          <Col>
            <Form.Group className="mb-3">
              <Form.Select
                aria-label="Select type"
                id="component_type_str"
                value={inputField.component_type_str}
                onChange={event => handleInputChange(index, event)}
              >
                <option value="EXTERNALLY_SOURCED">Externally Sourced</option>
                <option value="MADE_IN_HOUSE">Made In-House</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col>
            <Form.Group className="mb-3">
              <Form.Select
                aria-label="Select country"
                id="country_of_origin"
                value={inputField.country_of_origin}
                placeholder="Enter country of origin"
                onChange={event => handleInputChange(index, event)}
              >
                <option>Select country</option>
                {options.map((option, i) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </Form.Select>
            </Form.Group>
              { inputField.component_type_str === 'EXTERNALLY_SOURCED'
                ? <Form.Group>
                <Form.Label>Enter external SKU</Form.Label>
                <Typeahead
                  id="external_sku"
                  onInputChange={(text, event) => handleExternalSKUChange(index, text, event)}
                  options={sctrs.map(sctr => sctr.unique_identifier)}
                  placeholder="Enter external sku"
                />
              </Form.Group>
                : ' '
              }
          </Col>
          <Container>
            <Button onClick={() => handleAddFields()} className='me-2'>
              Add component
            </Button>
            <Button disabled={index === 0} onClick={() => handleRemoveFields(index)}>
              Remove component
            </Button>
          </Container>
        </Row>
      ))}

      <Button onClick={() => (setSubmitButton('publish'))} className="my-3 me-2" variant="primary" type="submit">
        Publish
      </Button>
      <Button onClick={() => (setSubmitButton('draft'))} className="my-3" variant="primary" type="submit">
        Create Draft
      </Button>
    </Form>
  )
}

export default SCTRForm
