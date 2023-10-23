/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState } from 'react'
import { Button, Form, Container, Row, Col } from 'react-bootstrap'
import { useNavigate } from 'react-router'
import CountrySelect from './CountrySelect'
import { Typeahead } from 'react-bootstrap-typeahead'
import ReactCountryFlag from 'react-country-flag'
import { calculateCOGS } from '../utils/Utilities'
import { useCountryListQuery } from '../api/CountryList'
import { useSearchOriginReportsQuery, useCreateOriginReport, useCreateOriginReportDraft } from '../api/OriginReport'
import LoadingComponent from './LoadingComponent'

const OriginReportForm = () => {
  const [inputFields, setInputFields] = useState([])

  const countryList = useCountryListQuery({
    onSuccess: (data) => {
      const defaultInputFields = {
        fraction_cogs: 0,
        short_description: '',
        component_type_str: 'MADE_IN_HOUSE',
        external_sku: '',
        // initialize to the first country returned by backend
        country_of_origin:
          (data.length > 0 ? data[0].alpha_2 : 'AF'),
        company_name: ''
      }
      setInputFields([defaultInputFields])
    }
  })
  // For different submits
  const [submitButton, setSubmitButton] = useState([{
    button: ''
  }])

  const navigate = useNavigate()

  const [query, setQuery] = React.useState({})
  const { isLoading, isError, data: availableOriginReports } = useSearchOriginReportsQuery({ query })

  const createOriginReport = useCreateOriginReport()
  const createOriginReportDraft = useCreateOriginReportDraft()

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    // set data value from the form
    const data = new FormData()

    data.append('unique_identifier', event.target.unique_identifier.value)
    data.append('unique_identifier_type_str', event.target.unique_identifier_type_str.value)
    data.append('short_description', event.target.short_description[0].value)
    if (event.target.thumbnail.files.length !== 0) {
      data.append('thumbnail', event.target.thumbnail.files[0])
    }

    inputFields.forEach((value, index) => {
      data.append(`components[${index}]fraction_cogs`, value.fraction_cogs)
      data.append(`components[${index}]short_description`, value.short_description)
      data.append(`components[${index}]component_type_str`, value.component_type_str)
      data.append(`components[${index}]external_sku`, value.external_sku)
      data.append(`components[${index}]country_of_origin`, value.country_of_origin)
      data.append(`components[${index}]company_name`, value.company_name)
    })

    const mutation = (submitButton === 'draft') ? createOriginReportDraft : createOriginReport

    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        alert('Successfully created')
        navigate('/account/origin_report')
      },
      onError: (error, variables, context) => {
        if (error.request?.status === 400) {
          const result = error.response.data

          let message = 'Invalid input data:'
          for (const invalidElement in result) {
            if (invalidElement === 'components') {
              if (Array.isArray(result.components)) {
                for (const index in result.components) {
                  for (const field in result.components[index]) {
                    message += '\n' + invalidElement + ' ' +
                      (+index + 1) + ': ' + field +
                      ' ' + result.components[index][field]
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
    })
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

    setQuery({ unique_identifier__icontains: text })
    // When user deletes all characters
    if (!text) {
      // If company name is set
      if (values[index].company_name) {
        setQuery({ company__name__icontains: values[index].company_name })
      } else {
        setQuery({})
      }
    }
    setInputFields(values)
  }

  const handleCompanyNameChange = (index, text, event) => {
    // event here doesn't have event.target.id
    const values = [...inputFields]
    values[index].company_name = text

    setQuery({ company__name__icontains: text })
    // When user deletes all characters
    if (!text) {
      // If external_sku is set
      if (values[index].external_sku) {
        setQuery({ unique_identifier__icontains: values[index].external_sku })
      } else {
        setQuery({})
      }
    }
    setInputFields(values)
  }

  if (countryList.isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (countryList.isError) {
    return (
      <h2 className="text-center">An error has occurred: { countryList.error.message }</h2>
    )
  } else {
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

        <Form.Group className="mb-3" controlId="thumbnail">
          <Form.Label>Thumbnail</Form.Label>
          <Form.Control type="file"/>
        </Form.Group>

        <p>COGS: {calculateCOGS(inputFields)}%</p>

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
                          options={Array.from(new Set(
                            (!isLoading && !isError)
                              ? availableOriginReports.map(originReport => originReport.company.name)
                              : []
                          ))}
                          placeholder="Enter company name"
                          isLoading={isLoading}
                          isInvalid={isError}
                        />
                      </Form.Group>
                      <Form.Group>
                        <Form.Label>Enter external SKU</Form.Label>
                        <Typeahead
                          id="external_sku"
                          onChange={(text, event) => handleExternalSKUChange(index, text[0], event)}
                          onInputChange={(text, event) => handleExternalSKUChange(index, text, event)}
                          options={
                            (!isLoading && !isError)
                              ? availableOriginReports.map(originReport => originReport.unique_identifier)
                              : []
                          }
                          placeholder="Enter external sku"
                          isLoading={isLoading}
                          isInvalid={isError}
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
}

export default OriginReportForm
