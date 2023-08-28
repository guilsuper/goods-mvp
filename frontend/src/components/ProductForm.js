/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { Fragment, useContext, useState, useMemo } from 'react'
import { Button, Form, Container } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router'
import countryList from 'react-select-country-list'

const ProductForm = () => {
  // authTokens are for sending request to the backend
  const { authTokens } = useContext(AuthContext)
  // all possible countries list
  const options = useMemo(() => countryList().getData(), [])
  const [inputFields, setInputFields] = useState([{
    fraction_cogs: '',
    marketing_name: '',
    component_type: ''
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
      response = await fetch('/api/product/create/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert('Successfully created')
      navigate('/account/products')
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
                message += '\n' + invalidElement + ': ' + field + ' ' + result.components[index][field]
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
      fraction_cogs: '',
      marketing_name: '',
      component_type: ''
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
      if (values[index].component_type === 'Made In-House') {
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

  return (
    <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="unique_identifier">
        <Form.Label>Unique identifier</Form.Label>
        <Form.Control type="text" placeholder="Enter unique identifier" />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Unique dentifier type</Form.Label>
        <Form.Select aria-label="Select type" id="unique_identifier_type">
          <option>Enter id type</option>
          <option value="SKU">SKU</option>
          <option value="GNIT">GNIT</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="marketing_name">
        <Form.Label>Marketing name</Form.Label>
        <Form.Control type="text" placeholder="Enter marketing name" />
      </Form.Group>

      {inputFields.map((inputField, index) => (
        <Fragment key={`${inputField}~${index}`}>
          <Container className='my-4 p-3 border rounded'>
            <Form.Group className="mb-3" controlId="fraction_cogs">
              <Form.Label>Fraction COGS</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter fraction COGS"
                value={inputField.fraction_cogs}
                onChange={event => handleInputChange(index, event)}
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="marketing_name">
              <Form.Label>Marketing name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Enter marketing name"
                value={inputField.marketing_name}
                onChange={event => handleInputChange(index, event)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Component type</Form.Label>
              <Form.Select
                aria-label="Select type"
                id="component_type"
                value={inputField.component_type}
                onChange={event => handleInputChange(index, event)}
              >
                <option>Enter component type</option>
                <option value="Made In-House">Made In-House</option>
                <option value="Externally Sourced">Externally Sourced</option>
              </Form.Select>
            </Form.Group>
            {
              inputField.component_type
                ? inputField.component_type === 'Externally Sourced'
                  ? <Form.Group className="mb-3" controlId="external_sku">
                    <Form.Label>External SKU</Form.Label>
                    <Form.Control
                      type="text"
                      value={inputField.external_sku}
                      placeholder="Enter external sku"
                      onChange={event => handleInputChange(index, event)}
                    />
                  </Form.Group>
                  : <Form.Group className="mb-3">
                      <Form.Label>Product country</Form.Label>
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

            <Button onClick={() => handleAddFields()}>
              Add component
            </Button>
            <Button disabled={index === 0} onClick={() => handleRemoveFields(index)}>
              Remove component
            </Button>
          </Container>
        </Fragment>
      ))}

      <Button className="my-3" variant="primary" type="submit">
        Create product
      </Button>
    </Form>
  )
}

export default ProductForm
