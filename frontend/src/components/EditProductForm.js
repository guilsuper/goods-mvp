/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState, useMemo } from 'react'
import { Button, Form, Container, Col, Row } from 'react-bootstrap'
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
  const [buttonType, setButtonType] = useState('')
  // If successfully editted, go to home page to prevent multiple editting
  const navigate = useNavigate()

  const [inputFields, setInputFields] = useState([{
    id: '',
    fraction_cogs: '',
    marketing_name: '',
    component_type: '',
    external_sku: '',
    country_of_origin: ''
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
        response = await fetch('/api/product/delete_retrieve/' + productIdentifier + '/', config)
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
        setInputFields(result.components)
      }
    }
    getProductInfo()
  }, [authTokens, navigate, productIdentifier])

  // Handle submit
  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const data = {
      unique_identifier: event.target.unique_identifier.value ? event.target.unique_identifier.value : product.unique_identifier,
      unique_identifier_type: event.target.unique_identifier_type.value ? event.target.unique_identifier_type.value : product.unique_identifier_type,
      marketing_name: event.target.marketing_name[0].value ? event.target.marketing_name[0].value : product.marketing_name
    }

    // Config for PATCH request
    const config = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }
    const configProduct = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      },
      body: JSON.stringify(data)
    }

    let response = ''
    let responseProduct = ''
    let responsesComponent = []

    let result = ''

    try {
      responseProduct = await fetch('/api/product/patch/' + productIdentifier + '/', configProduct)
      for (const index in inputFields) {
        const configComponent = {
          method: 'PATCH',
          headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + authTokens.access
          },
          body: JSON.stringify(inputFields[index])
        }
        const resonseComponent = await fetch('/api/component/patch_delete_retrieve/' + inputFields[index].id + '/', configComponent)
        responsesComponent = [...responsesComponent, resonseComponent]
      }

      if (buttonType !== 'draft') {
        response = await fetch('/api/product/to_published/' + productIdentifier + '/', config)
        const resultPublish = await response.json()

        if (response.status === 200) {
          alert('Successfully published')
          navigate('/products/' + productIdentifier)
        } else if (response.status === 400) {
          let message = 'Invalid input data:'
          message += JSON.stringify(resultPublish)
          alert(message)
        } else {
          alert('Not authenticated or permission denied')
          navigate('/')
        }
      }
    } catch (error) {
      alert('Server is not responding')
      return
    }

    result = await responseProduct.json()

    if (responseProduct.status === 200) {
      alert('Successfully editted')
      navigate('/products/' + productIdentifier)
    } else if (responseProduct.status === 400) {
      let message = 'Invalid input data:'
      message += JSON.stringify(result)
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
      navigate('/')
    }
  }

  // Handle adding a field
  const handleAddFields = async () => {
    const config = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/component/create/' + productIdentifier + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    const result = await response.json()

    if (response.status !== 200) {
      alert('Server is not responding')
    }
    const values = [...inputFields]
    values.push({
      id: result.id,
      fraction_cogs: 0,
      marketing_name: '',
      component_type: 'Made In-House',
      external_sku: '',
      country_of_origin: ''
    })

    setInputFields(values)
  }

  // Handle removing a field
  const handleRemoveFields = async (index) => {
    const componentId = inputFields[index].id

    const config = {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/component/patch_delete_retrieve/' + componentId + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    if (response.status !== 204) {
      alert('Server is not responding')
    }

    const values = [...inputFields]
    values.splice(index, 1)
    setInputFields(values)
  }

  const handleInputChange = (index, event) => {
    const values = [...inputFields]
    values[index][event.target.id] = event.target.value

    // If component type was changed
    if (event.target.id === 'component_type') {
      values[index].external_sku = ''
      values[index].country_of_origin = ''
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
                  <option value="Made In-House">Made In-House</option>
                  <option value="Externally Sourced">Externally Sourced</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col>
              {
                inputField.component_type
                  ? inputField.component_type === 'Externally Sourced'
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

        <Button onClick={() => (setButtonType('publish'))} className="my-3 me-2" variant="primary" type="submit">
          Publish
        </Button>
        <Button onClick={() => (setButtonType('draft'))} className="my-3" variant="primary" type="submit">
          Save draft
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditProductForm
