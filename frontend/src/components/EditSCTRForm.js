/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState, useMemo } from 'react'
import { Button, Form, Container, Col, Row } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import countryList from 'react-select-country-list'
import { toReadable } from '../utils/Utilities'

const EditSCTRForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  const { authTokens } = useContext(AuthContext)
  const { sctrIdentifier } = useParams()
  const [sctr, setSCTR] = useState([])

  const [buttonType, setButtonType] = useState('')
  // If successfully editted, go to home page to prevent multiple editting
  const navigate = useNavigate()

  // components input fields data
  const [inputFields, setInputFields] = useState([{
    id: 0,
    fraction_cogs: 0,
    marketing_name: '',
    component_type_str: '',
    external_sku: '',
    country_of_origin: ''
  }])

  const options = useMemo(() => countryList().getData(), [])

  // Get data about sctr
  useEffect(() => {
    async function getSCTRInfo () {
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
        response = await fetch('/api/sctr/delete_retrieve/' + sctrIdentifier + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        // set sctr, components and inputFields
        setSCTR(result)

        // Change component_type to component_type_str
        const data = []
        for (const index in result.components) {
          data.push({
            id: result.components[index].id,
            fraction_cogs: result.components[index].fraction_cogs,
            marketing_name: result.components[index].marketing_name,
            component_type_str: result.components[index].component_type,
            external_sku: result.components[index].external_sku,
            country_of_origin: result.components[index].country_of_origin
          })
        }
        setInputFields(data)
      }
    }
    getSCTRInfo()
  }, [authTokens, navigate, sctrIdentifier])

  // Handle submit
  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    // Get only not empty data
    const data = {
      unique_identifier:
        event.target.unique_identifier.value
          ? event.target.unique_identifier.value
          : sctr.unique_identifier,

      unique_identifier_type_str:
        event.target.unique_identifier_type_str.value
          ? event.target.unique_identifier_type_str.value
          : sctr.unique_identifier_type,

      marketing_name:
        event.target.marketing_name[0].value
          ? event.target.marketing_name[0].value
          : sctr.marketing_name
    }

    // Config for move to publish request
    const config = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    // config to update SCTR
    const configSCTR = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      },
      body: JSON.stringify(data)
    }

    // responses for each request
    let response = ''
    let responseSCTR = ''
    let responsesComponent = []

    try {
      // Save SCTR changes
      responseSCTR = await fetch('/api/sctr/patch/' + sctrIdentifier + '/', configSCTR)
      // Save component changes
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

        const resonseComponent = await fetch(
          '/api/component/patch_delete_retrieve/' + inputFields[index].id + '/',
          configComponent
        )
        responsesComponent = [...responsesComponent, resonseComponent]
      }

      // If PUBLISH button was pressed
      if (buttonType !== 'draft') {
        response = await fetch('/api/sctr/to_published/' + sctrIdentifier + '/', config)
        const resultPublish = await response.json()

        if (response.status === 200) {
          alert('Successfully saved and published')
          navigate('/sctr/' + sctrIdentifier)
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

    // If PUBLISH button pressed, do not display these messages
    if (buttonType !== 'draft') {
      return
    }

    const result = await responseSCTR.json()

    if (responseSCTR.status === 200) {
      alert('SCTR Successfully editted')
      navigate('/sctr/' + sctrIdentifier)
    } else if (responseSCTR.status === 400) {
      let message = 'Invalid input data:'
      message += JSON.stringify(result)
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
      navigate('/')
    }

    for (const index in responsesComponent) {
      if (responsesComponent[index].status === 200) {
        alert('Component #' + (1 + +index) + ' successfully editted')
        navigate('/sctr/' + sctrIdentifier)
      } else if (responsesComponent[index].status === 400) {
        let message = 'Invalid input data:'
        message += JSON.stringify(await responsesComponent[index].json())
        alert(message)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
  }

  // Handle adding a component fields
  // Creates a new component in the backed
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
      response = await fetch('/api/component/create/' + sctrIdentifier + '/', config)
    } catch (error) {
      alert('Server is not responding')
      return
    }

    const result = await response.json()

    if (response.status !== 200) {
      alert('Server is not responding')
      return
    }
    // Update inputFields
    const values = [...inputFields]
    values.push({
      id: result.id,
      fraction_cogs: result.fraction_cogs,
      marketing_name: result.marketing_name,
      component_type_str: result.component_type,
      external_sku: result.external_sku,
      country_of_origin: result.country_of_origin
    })
    setInputFields(values)
  }

  // Handle removing a field
  // Deletes component in the backend
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

  // Changes inputFields list
  const handleInputChange = (index, event) => {
    const values = [...inputFields]
    values[index][event.target.id] = event.target.value

    setInputFields(values)
  }

  // Quality of life feature, calculates all component COGS
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

  // If first component doesn't exist (data wasn't fetch)
  // SCTR always has at least 1 component
  if (!inputFields[0]) {
    return
  }

  return (
    <FormContainer>
      <Form onSubmit={submitHandler}>
        <Form.Group className="mb-3" controlId="unique_identifier">
          <Form.Label>Unique identifier</Form.Label>
          <Form.Control type="text" placeholder={sctr.unique_identifier} />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Unique identifier type</Form.Label>
          <Form.Select
            aria-label="Select type"
            id="unique_identifier_type_str"
          >
            <option>Select identifier type</option>
            <option value="SKU">SKU</option>
            <option value="GNIT">GNIT</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3" controlId="marketing_name">
          <Form.Label>Marketing name</Form.Label>
          <Form.Control type="text" placeholder={sctr.marketing_name} />
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
            <p>External SKU and country of origin</p>
          </Col>
        </Row>

        {inputFields.map((inputField, index) => (
          <Row key={`${inputField}~${index}`} className='mb-3 p-3 border rounded'>
            <Col>
              <Form.Group className="mb-3" controlId="fraction_cogs">
                <Form.Control
                  type="text"
                  placeholder={inputField.fraction_cogs}
                  value={inputField.fraction_cogs}
                  onChange={event => handleInputChange(index, event)}
                />
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="mb-3" controlId="marketing_name">
                <Form.Control
                  type="text"
                  placeholder={inputField.marketing_name}
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
                  onChange={event => handleInputChange(index, event)}
                >
                  <option>{toReadable(inputField.component_type_str)}</option>
                  <option value="EXTERNALLY_SOURCED">Externally Sourced</option>
                  <option value="MADE_IN_HOUSE">Made In-House</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col>
              <Form.Group className="mb-3" controlId="external_sku">
                <Form.Control
                  type="text"
                  value={inputField.external_sku}
                  placeholder={inputField.external_sku}
                  onChange={event => handleInputChange(index, event)}
                />
              </Form.Group>
                <Form.Group className="mb-3">
                  <Form.Select
                    aria-label="Select country"
                    id="country_of_origin"
                    onChange={event => handleInputChange(index, event)}
                  >
                    <option>{toReadable(inputField.country_of_origin)}</option>
                    {options.map((option, i) => (
                      <option key={option.value} value={option.value}>{option.label}</option>
                    ))}
                  </Form.Select>
                </Form.Group>
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

export default EditSCTRForm
