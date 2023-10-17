/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState } from 'react'
import { Button, Form, Container, Col, Row } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { useNavigate, useParams } from 'react-router-dom'
import FormContainer from '../utils/FormContainer'
import CountrySelect from './CountrySelect'
import { Typeahead } from 'react-bootstrap-typeahead'
import ReactCountryFlag from 'react-country-flag'
import ImageComponent from '../components/ImageComponent'
import { calculateCOGS } from '../utils/Utilities'

const EditOriginReportForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  const { authTokens } = useContext(AuthContext)
  const { originReportIdentifier } = useParams()
  const [originReport, setOriginReport] = useState([])

  const [buttonType, setButtonType] = useState('')
  // If successfully edited, go to home page to prevent multiple editing
  const navigate = useNavigate()

  // Variables to track components' changes
  const [inputFields, setInputFields] = useState([{
    id: 0,
    fraction_cogs: 0,
    short_description: '',
    component_type_str: 'MADE_IN_HOUSE',
    external_sku: '',
    country_of_origin: 'AF',
    company_name: '',
    parent_origin_report: 0,
    // Fields for tracking created and deleted components
    is_deleted: false,
    is_created: false
  }])

  // Are constant values that represents all existing published OriginReports
  const [originReports, setOriginReports] = useState([])
  // Will change depending on user's input in external_sku and company_name
  const [availableOriginReports, setAvailableOriginReport] = useState([])

  // Get data about originReport
  useEffect(() => {
    async function getOriginReportInfo () {
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
        response = await fetch('/api/origin_report/delete_retrieve/' + originReportIdentifier + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        // set originReport and components
        setOriginReport(result)

        // Change component_type to component_type_str
        const data = []
        for (const index in result.components) {
          data.push({
            id: result.components[index].id,
            fraction_cogs: result.components[index].fraction_cogs,
            short_description: result.components[index].short_description,
            component_type_str: result.components[index].component_type,
            external_sku: result.components[index].external_sku,
            country_of_origin: result.components[index].country_of_origin,
            company_name: result.components[index].company_name,
            is_deleted: false,
            is_created: false
          })
        }
        setInputFields(data)
      }
    }
    getOriginReportInfo()

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
        // Permanent data about available origin reports
        setOriginReports(data)
        // Initialize the set available origin reports. This set will
        // be filtered based on what the user searches for out of the
        // total set of origin reports.
        setAvailableOriginReport(data)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
    // Set all available OriginReports for a external sku field
    getOriginReports()
  }, [authTokens.access, navigate, originReportIdentifier])

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

    // Config for move to publish request
    const config = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    // config to update OriginReport
    const configOriginReport = {
      method: 'PATCH',
      headers: {
        Authorization: 'Bearer ' + authTokens.access
      },
      body: data
    }

    // responses for each request
    let response = ''
    let responseOriginReport = ''
    let responsesComponent = []

    // Save OriginReport changes
    responseOriginReport = await fetch('/api/origin_report/patch/' + originReportIdentifier + '/', configOriginReport)
    // Delete components
    const componentToDelete = inputFields.filter(component => component.is_deleted === true)
    for (const index in componentToDelete) {
      const componentId = componentToDelete[index].id

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
        window.location.reload()
      }

      if (response.status === 204) {
        alert('Successfully deleted #' + componentId)
      } else {
        alert('Failed to delete #' + componentId)
        window.location.reload()
      }
    }
    // Create components
    const componentToCreate = inputFields.filter(component => component.is_created === true)
    for (const index in componentToCreate) {
      componentToCreate[index].parent_origin_report = originReport.id

      const config = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + authTokens.access
        },
        body: JSON.stringify(componentToCreate[index])
      }

      let response = ''
      try {
        response = await fetch('/api/component/create_draft/', config)
      } catch (error) {
        alert('Server is not responding')
        window.location.reload()
      }
      const result = await response.json()
      if (response.status === 201) {
        alert('Successfully created #' + result.id)
      } else {
        let message = 'Invalid create data #' + index
        for (const invalidElement in result) {
          message += '\n' + invalidElement + ': ' + result[invalidElement]
        }
        alert(message)
        window.location.reload()
      }
    }
    // Save component changes
    // If components.id > 0, then it was retrieved from the backend and should be updated
    const componentToSave = inputFields.filter(component => (component.id && !component.is_deleted))
    for (const index in componentToSave) {
      const configComponent = {
        method: 'PATCH',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + authTokens.access
        },
        body: JSON.stringify(componentToSave[index])
      }

      const responseComponent = await fetch(
        '/api/component/patch_delete_retrieve/' + componentToSave[index].id + '/',
        configComponent
      )
      responsesComponent = [...responsesComponent, responseComponent]
    }

    // If PUBLISH button was pressed
    if (buttonType !== 'draft') {
      response = await fetch('/api/origin_report/to_published/' + originReportIdentifier + '/', config)
      const resultPublish = await response.json()

      if (response.status === 200) {
        alert('Successfully saved and published')
        navigate('/origin_report/' + originReportIdentifier)
      } else if (response.status === 400) {
        let message = 'Invalid save data:'
        message += JSON.stringify(resultPublish)
        alert(message)
        window.location.reload()
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }

    // If PUBLISH button pressed, do not display these messages
    if (buttonType !== 'draft') {
      return
    }

    const result = await responseOriginReport.json()

    if (responseOriginReport.status === 200) {
      alert('Origin Report Successfully edited')
      navigate('/origin_report/' + originReportIdentifier)
    } else if (responseOriginReport.status === 400) {
      let message = 'Invalid origin report data:'
      message += JSON.stringify(result)
      alert(message)
    } else {
      alert('Not authenticated or permission denied')
      navigate('/')
    }

    for (const index in responsesComponent) {
      if (responsesComponent[index].status === 200) {
        alert('Component #' + (1 + +index) + ' successfully edited')
        navigate('/origin_report/' + originReportIdentifier)
      } else if (responsesComponent[index].status === 400) {
        let message = 'Invalid save component data #' + index
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
    // Update inputFields
    const values = [...inputFields]
    values.push({
      id: 0,
      fraction_cogs: 0,
      short_description: '',
      component_type_str: 'MADE_IN_HOUSE',
      external_sku: '',
      country_of_origin: 'AF',
      company_name: '',
      parent_origin_report: 0,
      // Fields for tracking created and deleted components
      is_deleted: false,
      is_created: true
    })
    setInputFields(values)
    console.log(inputFields)
  }

  // Handle removing a component
  const handleRemoveFields = async (index) => {
    // id != 0 means that component exists in the DB
    // So we need to remove it in the DB
    const values = [...inputFields]
    console.log(index)
    if (values[index].id !== 0) {
      values[index].is_deleted = true
    } else {
      // If component was created in the form
      // Remove it from components array
      values.splice(index, 1)
    }
    setInputFields(values)
    console.log(inputFields)
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

  // If first component doesn't exist (data wasn't fetch)
  // OriginReport always has at least 1 component
  if (!inputFields[0]) {
    return
  }

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
            ? <ImageComponent src={originReport.thumbnail_url} text={'Thumbnail'}/>
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
                        options={Array.from(new Set(availableOriginReports.map(originReport => originReport.company.name)))}
                        placeholder={inputField.company_name}
                      />
                    </Form.Group>
                    <Form.Group>
                      <Form.Label>Enter external SKU</Form.Label>
                      <Typeahead
                        id="external_sku"
                        onChange={(text, event) => handleExternalSKUChange(index, text[0], event)}
                        onInputChange={(text, event) => handleExternalSKUChange(index, text, event)}
                        options={availableOriginReports.map(originReport => originReport.unique_identifier)}
                        placeholder={inputField.external_sku}
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

export default EditOriginReportForm
