/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState, Fragment, useMemo } from 'react'
import { Button, Form, Container } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import countryList from 'react-select-country-list'

const EditProductForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  const { authTokens } = useContext(AuthContext)
  const { productIdentifier } = useParams()
  const [product, setProduct] = useState([])
  // If successfully editted, go to home page to prevent multiple editting
  const navigate = useNavigate()

  const [inputFields, setInputFields] = useState([{
    fraction_cogs: '',
    marketing_name: '',
    component_type: ''
  }])

  const options = useMemo(() => countryList().getData(), [])

  useEffect(() => {
    async function getProductInfo () {
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
        response = await fetch('/api/product/patch_delete_retrieve/' + productIdentifier + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        setProduct(result)

        // parse components
        for (const component in result.components) {
          for (const field in result.components[component]) {
            if (!result.components[component][field]) {
              delete result.components[component][field]
            }
          }
        }

        setInputFields(result.components)
      }
    }
    getProductInfo()
  }, [authTokens, navigate, productIdentifier])
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
      response = await fetch('/api/product/patch_delete_retrieve/' + productIdentifier + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    const result = await response.json()

    if (response.status === 200) {
      alert('Successfully editted')
      navigate('/products/' + productIdentifier)
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
                message += '\n' + invalidElement + ' ' + (Number(index) + 1) + ': ' + field + ' ' + result.components[index][field]
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
      navigate('/')
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
    <FormContainer>
      <Form onSubmit={submitHandler}>
        <Form.Group className="mb-3" controlId="unique_identifier">
          <Form.Label>Unique identifier</Form.Label>
          <Form.Control type="text" placeholder={product.unique_identifier} />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Unique dentifier type</Form.Label>
          <Form.Select aria-label="Select type" id="unique_identifier_type">
            <option>{product.unique_identifier_type}</option>
            <option value="SKU">SKU</option>
            <option value="GNIT">GNIT</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3" controlId="marketing_name">
          <Form.Label>Marketing name</Form.Label>
          <Form.Control type="text" placeholder={product.marketing_name} />
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
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditProductForm
