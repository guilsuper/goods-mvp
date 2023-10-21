/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState } from 'react'
import { Button, Form, Container, Col, Row } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import CountrySelect from './CountrySelect'
import { Typeahead } from 'react-bootstrap-typeahead'
import ReactCountryFlag from 'react-country-flag'
import ImageComponent from '../components/ImageComponent'
import { calculateCOGS } from '../utils/Utilities'
import { useCountryListQuery } from '../api/CountryList'
import { useEditOriginReportDraft, usePublishOriginReport, useGetOriginReportQuery, useSearchOriginReportsQuery } from '../api/OriginReport'
import LoadingComponent from './LoadingComponent'

const EditOriginReportForm = () => {
  const { originReportIdentifier } = useParams()

  const { isLoading, isError, data: originReport, error } =
        useGetOriginReportQuery({
          id: originReportIdentifier,
          onSuccess: (data) => {
            // initialize all initial component data
            const inputFieldData = []
            for (const index in data.components) {
              inputFieldData.push({
                fraction_cogs: data.components[index].fraction_cogs,
                short_description: data.components[index].short_description,
                component_type_str: data.components[index].component_type,
                external_sku: data.components[index].external_sku,
                country_of_origin: data.components[index].country_of_origin,
                company_name: data.components[index].company_name
              })
            }
            setInputFields(inputFieldData)
          }
        })

  const countryList = useCountryListQuery({})

  const editOriginReportDraft = useEditOriginReportDraft()
  const publishOriginReport = usePublishOriginReport()

  const [buttonType, setButtonType] = useState('')
  // If successfully edited, go to home page to prevent multiple editing
  const navigate = useNavigate()

  // Variables to track components' changes; This is left
  // uninitialized; useGetOriginReportQuery fills it in when the OR
  // loads
  const [inputFields, setInputFields] = useState([])

  const [query, setQuery] = React.useState({})
  const availableOriginReports = useSearchOriginReportsQuery({ query })

  // Handle submit
  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    // Get only not empty data
    const data = new FormData()
    if (event.target.unique_identifier.value) {
      data.append('unique_identifier', event.target.unique_identifier.value)
    }
    if (event.target.unique_identifier_type_str.value) {
      data.append('unique_identifier_type_str', event.target.unique_identifier_type_str.value)
    }
    if (event.target.short_description[0].value) {
      data.append('short_description', event.target.short_description[0].value)
    }
    // Handle the file input
    if (event.target.thumbnail.files.length !== 0) {
      data.append('thumbnail', event.target.thumbnail.files[0])
    }

    data.append('components', JSON.stringify(inputFields))

    editOriginReportDraft.mutate({ id: originReportIdentifier, parameters: data }, {

      // successful save of draft
      onSuccess: (dataDraft, { id, parameters }, contextDraft) => {
        // If PUBLISH button was pressed
        if (buttonType !== 'draft') {
          publishOriginReport.mutate(originReportIdentifier, {
            onSuccess: (dataPublish, id, contextPublish) => {
              alert('Successfully saved and published')
              navigate(`/origin_report/${id}`)
            },

            onError: (error, { id, parameters }, context) => {
              if (error.request?.status === 400) {
                let message = 'Invalid save data:'
                message += JSON.stringify(error.response.data)
                alert(message)
              } else {
                alert('Not authenticated or permission denied')
                navigate('/')
              }
            }
          })
        // if save draft was pressed
        } else {
          alert('Origin Report Successfully edited')
          navigate(`/origin_report/${id}`)
        }
      },

      // error saving draft
      onError: (errorDraft, { id, parameters }, context) => {
        if (errorDraft.request?.status === 400) {
          let message = 'Invalid origin report data:'
          message += JSON.stringify(error.resultpublish)
          alert(message)
        } else {
          alert('Not authenticated or permission denied')
          navigate('/')
        }
      }
    })
  }

  // Handle adding a component fields
  const handleAddFields = async () => {
    // Update inputFields
    const values = [...inputFields]
    values.push({
      fraction_cogs: 0,
      short_description: '',
      component_type_str: 'MADE_IN_HOUSE',
      external_sku: '',
      // initialize to the first country returned by backend
      country_of_origin:
        ((countryList.isSuccess && countryList.data.length > 0) ? countryList.data[0].alpha_2 : 'AF'),
      company_name: ''
    })
    setInputFields(values)
  }

  // Handle removing a component
  const handleRemoveFields = async (index) => {
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

  if (isLoading || countryList.isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (isError || countryList.isError) {
    return (
      <h2 className="text-center">An error has occurred: { error.message }</h2>
    )
  } else {
    return (
      <FormContainer>
        <Form onSubmit={submitHandler}>
          <Form.Group className="mb-3">
            <Form.Label>Identifier type</Form.Label>
            <Form.Select
              aria-label="Select type"
              id="unique_identifier_type_str"
              value={originReport.unique_identifier_type}
            >
              <option value="SKU">SKU</option>
              <option value="GTIN">GTIN</option>
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3" controlId="unique_identifier">
            <Form.Label>Identifier</Form.Label>
            <Form.Control type="text" placeholder={originReport.unique_identifier} />
          </Form.Group>

          <Form.Group className="mb-3" controlId="short_description">
            <Form.Label>Short description</Form.Label>
            <Form.Control type="text" placeholder={originReport.short_description} />
          </Form.Group>

          {
            // If logo is set
            originReport.thumbnail
              ? <ImageComponent src={originReport.ythumbnail_url} text={'Thumbnail'}/>
              : ' '
          }

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
            <Row
              key={`${inputField}~${index}`}
              // Display only not deleted components
              className={'mb-3 p-3 border rounded' + (inputField.is_deleted ? ' d-none' : '')}
            >
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
                <Form.Group className="mb-3" controlId="short_description">
                  <Form.Control
                    type="text"
                    placeholder={inputField.short_description}
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
                    onChange={event => handleInputChange(index, event)}
                    value={inputField.component_type_str}
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
                            (!availableOriginReports.isLoading && !availableOriginReports.isError)
                              ? availableOriginReports.data.map(originReport => originReport.company.name)
                              : []
                          ))}
                          isLoading={availableOriginReports.isLoading}
                          isinvalid={availableOriginReports.isError}
                        />
                      </Form.Group>
                      <Form.Group>
                        <Form.Label>Enter external SKU</Form.Label>
                        <Typeahead
                          id="external_sku"
                          onChange={(text, event) => handleExternalSKUChange(index, text[0], event)}
                          onInputChange={(text, event) => handleExternalSKUChange(index, text, event)}
                          options={
                            (!availableOriginReports.isLoading && !availableOriginReports.isError)
                              ? availableOriginReports.data.map(originReport => originReport.unique_identifier)
                              : []
                          }
                          placeholder={inputField.external_sku}
                          isLoading={availableOriginReports.isLoading}
                          isInvalid={availableOriginReports.isError}
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
                <Button
                  disabled={
                    // If there is more then 1 displayed components
                    (inputFields.length - inputFields.filter(component => component.is_deleted).length) <= 1
                  }
                  onClick={() => handleRemoveFields(index)}
                >
                  Remove component
                </Button>
              </Container>
            </Row>
          ))}
          <Container>
            <Button onClick={() => handleAddFields()} className='me-2' variant='secondary'>
              Add component
            </Button>
          </Container>
          <Button onClick={() => (setButtonType('publish'))} className="my-3 me-2" variant="success" type="submit">
            Publish
          </Button>
          <Button onClick={() => (setButtonType('draft'))} className="my-3" variant="primary" type="submit">
            Save draft
          </Button>
        </Form>
      </FormContainer>
    )
  }
}

export default EditOriginReportForm
