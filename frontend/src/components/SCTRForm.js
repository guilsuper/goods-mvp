/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState, useMemo } from 'react'
import { Button, Form, Container, Row, Col } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router'
import countryList from 'react-select-country-list'

const SCTRForm = () => {
  // authTokens are for sending request to the backend
  const { authTokens } = useContext(AuthContext)
  // all possible countries list
  const options = useMemo(() => countryList().getData(), [])
  const [inputFields, setInputFields] = useState([{
    fraction_cogs: 0,
    marketing_name: '',
    component_type: '1'
  }])
  const [submitButton, setSubmitButton] = useState([{
    button: ''
  }])

  const navigate = useNavigate()

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
        // Server response may send a key with error, that doesn't match the id of the element
        if (typeof event.target[invalidElement] !== 'undefined') {
          event.target[invalidElement].style = 'border-color: red'
        }
        // special case for the marketing_name
        if (invalidElement === 'marketing_name') {
          event.target[invalidElement][0].style = 'border-color: red'
        }

        if (invalidElement === 'components') {
          if (Array.isArray(result.components)) {
            for (const index in result.components) {
              for (const field in result.components[index]) {
                message += '\n' + invalidElement + ' ' + index + ': ' + field + ' ' + result.components[index][field]
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
      component_type: '1'
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

    // If component type was changed
    if (event.target.id === 'component_type') {
      if (values[index].component_type === '2') {
        if (typeof values[index].external_sku !== 'undefined') {
          delete values[index].external_sku
        }
        values[index].country_of_origin = ''
      } else {
        if (typeof values[index].country_of_origin !== 'undefined') {
          delete values[index].country_of_origin
        }
        values[index].external_sku = ''
      }
    }

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
        <Form.Label>Unique identifier</Form.Label>
        <Form.Control type="text" placeholder="Enter unique identifier" />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Unique dentifier type</Form.Label>
        <Form.Select aria-label="Select type" id="unique_identifier_type">
          <option value="1">SKU</option>
          <option value="2">GNIT</option>
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
          <p>External SKU or country of origin</p>
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
                id="component_type"
                value={inputField.component_type}
                onChange={event => handleInputChange(index, event)}
              >
                <option value="1">Externally Sourced</option>
                <option value="2">Made In-House</option>
              </Form.Select>
            </Form.Group>
          </Col>
          <Col>
            {
              inputField.component_type
                ? inputField.component_type === '1'
                  ? <Form.Group className="mb-3" controlId="external_sku">
                    <Form.Control
                      type="text"
                      value={inputField.external_sku}
                      placeholder="Enter external sku"
                      onChange={event => handleInputChange(index, event)}
                    />
                  </Form.Group>
                  : <Form.Group className="mb-3">
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
