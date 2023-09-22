/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState } from 'react'
import { Col, Row, Container, Button } from 'react-bootstrap'
import { useNavigate, useParams, Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { toReadable } from '../utils/Utilities'
import ReactCountryFlag from 'react-country-flag'
import countryList from 'react-select-country-list'

const SCTRInfo = () => {
  const { user, authTokens } = useContext(AuthContext)
  const { sctrIdentifier } = useParams()
  const [sctr, setSCTR] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getSCTRInfo () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      }
      // Set authorization if exists
      if (authTokens) {
        config.headers.Authorization = 'Bearer ' + authTokens.access
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
        setSCTR(result)
      }
    }
    getSCTRInfo()
  }, [navigate, sctrIdentifier])

  const isOwner = (user) => {
    // If not authorized
    if (!user) {
      return false
    }
    return (user.company.name === sctr.company.name)
  }

  const deleteSCTR = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete this SCTR?')) {
      return
    }

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
      response = await fetch('/api/sctr/delete_retrieve/' + sctrIdentifier + '/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 204) {
      alert('Successfully deleted')
      navigate('/account/sctr')
    } else {
      alert("Wasn't deleted or permission denied")
    }
  }

  const moveToDraft = async (event) => {
    const config = {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/sctr/to_draft/' + sctrIdentifier + '/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 200) {
      alert('Successfully moved')
      navigate('/account/sctr')
    } else {
      alert("Wasn't moved or permission denied")
    }
  }

  // If SCTR company wasn't loaded yet
  // When page renders, sctr.company is undefined
  // And it is impossible to get sctr.company.name for example
  if (!sctr.company) {
    return
  }

  const calculateCOGS = () => {
    const sum = sctr.components.reduce(function (prev, current) {
      return prev + +current.fraction_cogs
    }, 0)
    // If NaN
    if (!sum) {
      return 0
    }
    return sum
  }

  const switchVisibility = async () => {
    const config = {
      method: 'PUT',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/sctr/switch_visibility/' + sctrIdentifier + '/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 200) {
      alert('Successfully switched visibility')
      window.location.reload()
    } else {
      alert("Visibility wasn't switched")
    }
  }

  return (
    <Container>
      <h3 className='text-center'>Origin Report</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>Identifier Type</p></Row>
        <Row><p>{sctr.unique_identifier_type}</p></Row>

        <Row className='text-secondary'><p>Identifier</p></Row>
        <Row><p>{sctr.unique_identifier}</p></Row>

        <Row className='text-secondary'><p>Short Description</p></Row>
        <Row><p>{sctr.marketing_name}</p></Row>

        {
            isOwner(user)
              ? <>
              <Row className='text-secondary'><p>Is latest version</p></Row>
              <Row><p>{sctr.is_latest_version ? 'True' : 'False'}</p></Row>
              <Row className='text-secondary'><p>State</p></Row>
              <Row><p>{toReadable(sctr.state)}</p></Row>
              <Row className='text-secondary'><p>Version</p></Row>
              <Row><p>{sctr.version}</p></Row>
            </>
              : ' '
        }

        <p className='text-secondary'>COGS: {calculateCOGS()}%</p>

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

        {sctr.components.map((component, index) => (
        <Row key={`${component}~${index}`} className='mb-3 pt-2 ps-4 border rounded'>
          <Col><p>{component.fraction_cogs}</p></Col>

          <Col><p>{component.marketing_name}</p></Col>

          <Col>
            <Row><p>{toReadable(component.component_type)}</p></Row>
            <Row><p>{component.company_name}</p></Row>
            <Row><p>{component.external_sku}</p></Row>
          </Col>

          <Col><p>{countryList().getLabel(component.country_of_origin)}</p></Col>
          <Col className='d-flex align-items-center justify-content-center'>
            <ReactCountryFlag
              countryCode={component.country_of_origin}
              svg
              style={{
                width: '6.6em',
                height: '5em',
                border: '1px solid #dee2e6'
              }}
              title={component.country_of_origin}
            />
          </Col>
        </Row>
        ))}

        {
          isOwner(user)
            ? <Col className='w-25 mt-4'>
            <Row className='mb-3'>
              {
                sctr.state === 'DRAFT'
                  ? <>
                    <Button
                      variant='primary'
                      as={Link}
                      to={'/account/sctr/edit/' + sctr.id}
                    >Edit</Button>
                  </>
                  : <>
                    <Button variant='primary' onClick={moveToDraft}>Move to draft</Button>
                  </>
              }
            </Row>

            <Row>
              <Button variant='danger' onClick={deleteSCTR}>Delete SCTR</Button>
            </Row>

            {
              sctr.state !== 'DRAFT'
                ? <Row className='mt-3'>
                {
                  sctr.state === 'HIDDEN'
                    ? <>
                      <Button variant='secondary' onClick={switchVisibility}>Unhide</Button>
                    </>
                    : <>
                      <Button variant='secondary' onClick={switchVisibility}>Hide</Button>
                    </>
                }
                </Row>
                : ' '
            }

          </Col>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default SCTRInfo
