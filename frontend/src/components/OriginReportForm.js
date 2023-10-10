/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState, useEffect } from 'react'
import { Button, Form, Container, Row, Col } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate } from 'react-router'
import CountrySelect from './CountrySelect'
import { Typeahead } from 'react-bootstrap-typeahead'
import ReactCountryFlag from 'react-country-flag'

const OriginReportForm = () => {
  // authTokens are for sending request to the backend
  const { authTokens } = useContext(AuthContext)
  // all possible countries list
  const [inputFields, setInputFields] = useState([{
    fraction_cogs: 0,
    short_description: '',
    component_type_str: 'EXTERNALLY_SOURCED',
    external_sku: '',
    country_of_origin: '',
    company_name: ''
  }])
  // For different submits
  const [submitButton, setSubmitButton] = useState([{
    button: ''
  }])
  // Are constant values that represents all existing published OriginReports
  const [originReports, setOriginReports] = useState([])
  // Will change depending on user's input in external_sku and company_name
  const [availableOriginReports, setAvailableOriginReport] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getOriginReports () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      }
      let response = ''
      try {
        response = await fetch('/api/origin_report/get/', config)
      } catch (error) {
        alert('Server is not responding')
        return
      }
      const data = await response.json()

      if (response.status === 200) {
        // Set all available OriginReports for a external sku field
        setOriginReports(data)
        // Set available choices that depends on external sku field and company name
        setAvailableOriginReport(data)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
    getOriginReports()
  }, [setOriginReports, navigate])

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    // set data value from the form
    const data = {
      unique_identifier:
        event.target.unique_identifier.value,

      unique_identifier_type_str:
        event.target.unique_identifier_type_str.value,

      short_description:
        event.target.short_description[0].value
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
        response = await fetch('/api/origin_report/create_draft/', config)
      } else {
        response = await fetch('/api/origin_report/create/', config)
      }
    } catch (error) {
      alert('Server is not working')
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert('Successfully created')
      navigate('/account/origin_report')
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
      short_description: '',
      component_type_str: 'EXTERNALLY_SOURCED',
      external_sku: '',
      country_of_origin: '',
      company_name: ''
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

    setAvailableOriginReport(originReports.filter(originReport => originReport.unique_identifier === text))
    // When user deletes all characters
    if (!text) {
      // If company name is set
      if (values[index].company_name) {
        setAvailableOriginReport(originReports.filter(originReport => originReport.company.name === values[index].company_name))
      } else {
        setAvailableOriginReport(originReports)
      }
    }
    setInputFields(values)
  }

  const handleCompanyNameChange = (index, text, event) => {
    // event here doesn't have event.target.id
    const values = [...inputFields]
    values[index].company_name = text

    setAvailableOriginReport(originReports.filter(originReport => originReport.company.name === text))
    // When user deletes all characters
    if (!text) {
      // If external_sku is set
      if (values[index].external_sku) {
        setAvailableOriginReport(originReports.filter(originReport => originReport.unique_identifier === values[index].external_sku))
      } else {
        setAvailableOriginReport(originReports)
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
      <Form.Group className="mb-3">
        <Form.Label>Identifier Type</Form.Label>
        <Form.Select aria-label="Select type" id="unique_identifier_type_str">
          <option value="SKU">SKU</option>
          <option value="GTIN">GTIN</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="unique_identifier">
        <Form.Label>Identifier</Form.Label>
        <Form.Control type="text" placeholder="Enter SKU or GTIN (unique identifier)" />
      </Form.Group>

      <Form.Group className="mb-3" controlId="short_description">
        <Form.Label>Short Description</Form.Label>
        <Form.Control type="text" placeholder="Enter short description" />
      </Form.Group>

      <p>COGS: {calculateCOGS()}%</p>

      <Row className='mt-4'>
        <Col className='ps-4'>
          <p className="text-center">Fraction of COGS</p>
        </Col>
        <Col className='ps-4'>
          <p className="text-center">Short Description</p>
        </Col>
        <Col className='ps-4'>
          <p className="text-center">Component type (Company Name & External SKU)</p>
        </Col>
        <Col className='ps-4'>
          <p className="text-center">Country of origin</p>
        </Col>
        <Col className='ps-4'>
          <p className="text-center">Country flag</p>
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
            <Form.Group className="mb-3" controlId="short_description">
              <Form.Control
                type="text"
                placeholder="Enter short description"
                value={inputField.short_description}
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
              <CountrySelect
                id={'country_of_origin'}
                value={inputField.country_of_origin}
                onChange={event => handleInputChange(index, event)}
              />
            </Form.Group>
              { inputField.component_type_str === 'EXTERNALLY_SOURCED'
                ? <>
                    <Form.Group>
                      <Form.Label>Enter Company Name</Form.Label>
                      <Typeahead
                        id="company_name"
                        onChange={(text, event) => handleCompanyNameChange(index, text[0], event)}
                        onInputChange={(text, event) => handleCompanyNameChange(index, text, event)}
                        // Get only unique values (company names) and cast to Array to use filter function
                        options={Array.from(new Set(availableOriginReports.map(originReport => originReport.company.name)))}
                        placeholder="Enter company name"
                      />
                    </Form.Group>
                    <Form.Group>
                      <Form.Label>Enter external SKU</Form.Label>
                      <Typeahead
                        id="external_sku"
                        onChange={(text, event) => handleExternalSKUChange(index, text[0], event)}
                        onInputChange={(text, event) => handleExternalSKUChange(index, text, event)}
                        options={availableOriginReports.map(originReport => originReport.unique_identifier)}
                        placeholder="Enter external sku"
                      />
                    </Form.Group>
                </>
                : ' '
              }
          </Col>
          <Col className='d-flex align-items-center justify-content-center'>
            { inputField.country_of_origin
              ? <ReactCountryFlag
                  countryCode={inputField.country_of_origin}
                  svg
                  style={{
                    width: '6.6em',
                    height: '5em',
                    border: '1px solid #dee2e6'
                  }}
                  title={inputField.country_of_origin}
                />
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

export default OriginReportForm
