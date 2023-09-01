/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState, Fragment } from 'react'
import { Col, Row, Container, Button } from 'react-bootstrap'
import { useNavigate, useParams, Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

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
      window.location.reload()
    } else {
      alert("Wasn't moved or permission denied")
    }
  }

  // If SCTR company wasn't loaded yet
  // When page renders, sctr.company is undefiend
  // And it is imposible to get sctr.company.name for example
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
      <h3 className='text-center'>SCTR information</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>Unique identifier</p></Row>
        <Row><p>{sctr.unique_identifier}</p></Row>

        <Row className='text-secondary'><p>Unique dentifier type</p></Row>
        <Row><p>{sctr.unique_identifier_type}</p></Row>

        <Row className='text-secondary'><p>Marketing name</p></Row>
        <Row><p>{sctr.marketing_name}</p></Row>

        {
            isOwner(user)
              ? <>
              <Row className='text-secondary'><p>State</p></Row>
              <Row><p>{sctr.state}</p></Row>
            </>
              : ' '
        }

        <p className='text-secondary'>COGS: {calculateCOGS()}%</p>

        <Row className='mt-4'>
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

        {sctr.components.map((component, index) => (
        <Row key={`${component}~${index}`} className='mb-3 pt-2 ps-4 border rounded'>
          <Col><p>{component.fraction_cogs}</p></Col>

          <Col><p>{component.marketing_name}</p></Col>

          <Col><p>{component.component_type}</p></Col>

          {
            (component.component_type === 2)
              ? <>
                <Col><p>{component.country_of_origin}</p></Col>
              </>
              : <>
                <Col><p>{component.external_sku}</p></Col>
              </>
          }
        </Row>
        ))}

        {
          isOwner(user)
            ? <Col className='w-25 mt-4'>
            <Row className='mb-3'>
              {
                sctr.state === 1
                  ? <>
                    <Button
                      variant='primary'
                      as={Link}
                      to={'/account/sctr/edit/' + sctr.unique_identifier}
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
              sctr.state !== 1
                ? <Row className='mt-3'>
                {
                  sctr.state === 3
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
