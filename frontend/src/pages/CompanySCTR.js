/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect, useContext } from 'react'
import ListItem from '../components/ListItem'
import { Col, Container, Form, Row, Button } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'

const CompanySCTR = () => {
  const [sctrs, setSCTRs] = useState([])
  const { user, authTokens } = useContext(AuthContext)

  const navigate = useNavigate()

  useEffect(() => {
    async function getSCTRs () {
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
        response = await fetch('/api/sctr/get_by_company/', config)
      } catch (error) {
        alert('Server is not responding')
        return
      }
      const data = await response.json()

      if (response.status === 200) {
        setSCTRs(data)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
    getSCTRs()
  }, [user])

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const params = {}

    Object.keys(event.target).forEach(function (attr) {
      if (!isNaN(attr)) {
        params[event.target[attr].id] = event.target[attr].value
      }
    })

    let query = '?'
    Object.keys(params).forEach(function (param) {
      if (params[param]) {
        query += param + '=' + params[param] + '&'
      }
    })
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
      response = await fetch('/api/sctr/get/' + query, config)
    } catch (error) {
      alert('Server is not responding')
      return
    }
    const result = await response.json()
    setSCTRs(result)
  }

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
          <Row className='mt-2'>
            <p className='text-center'>Filters</p>
          </Row>
          <Container className="align-items-center py-2">
            <Form onSubmit={submitHandler}>
              <Form.Group className="mb-3" controlId="unique_identifier__icontains">
                <Form.Label>Unique identifier contains...</Form.Label>
                <Form.Control type="text" placeholder="Enter id" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="marketing_name__icontains">
                <Form.Label>Public facing id contains...</Form.Label>
                <Form.Control type="text" placeholder="Enter marketing name" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="cogs__lte">
                <Form.Label>SCTR COGS less than...</Form.Label>
                <Form.Control type="text" placeholder="Enter SCTR COGS" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="cogs__gte">
                <Form.Label>SCTR COGS greater than...</Form.Label>
                <Form.Control type="text" placeholder="Enter SCTR COGS" />
              </Form.Group>

              <Button variant="primary" type="submit">
                Filter
              </Button>
              <Button
                variant="secondary"
                as={Link}
                to="/account/sctr/create"
                className='ms-1'
              >Create</Button>
            </Form>
          </Container>
        </Col>
        <Col>
          <Row className="justify-content-md-center">
            {sctrs.map((sctr, index) => (
              <ListItem key={index} sctr={sctr}/>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  )
}

export default CompanySCTR
