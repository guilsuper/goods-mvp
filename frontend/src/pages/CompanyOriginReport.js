/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect, useContext } from 'react'
import ListItem from '../components/ListItem'
import { Col, Container, Form, Row, Button } from 'react-bootstrap'
import AuthContext from '../context/AuthContext'
import { Link, useNavigate } from 'react-router-dom'

const CompanyOriginReport = () => {
  const [originReports, setOriginReports] = useState([])
  const { user, authTokens } = useContext(AuthContext)

  const navigate = useNavigate()

  useEffect(() => {
    async function getOriginReports () {
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
        response = await fetch('/api/origin_report/get_by_company/', config)
      } catch (error) {
        alert('Server is not responding')
        return
      }
      const data = await response.json()

      if (response.status === 200) {
        setOriginReports(data)
      } else {
        alert('Not authenticated or permission denied')
        navigate('/')
      }
    }
    getOriginReports()
  }, [user, authTokens, navigate])

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
      response = await fetch('/api/origin_report/get/' + query, config)
    } catch (error) {
      alert('Server is not responding')
      return
    }
    const result = await response.json()
    setOriginReports(result)
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
                <Form.Label>SKU contains...</Form.Label>
                <Form.Control type="text" placeholder="SKU" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="short_description__icontains">
                <Form.Label>Short description...</Form.Label>
                <Form.Control type="text" placeholder="short description" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="cogs__lte">
                <Form.Label>COGS less than...</Form.Label>
                <Form.Control type="text" placeholder="Enter COGS" />
              </Form.Group>

              <Form.Group className="mb-3" controlId="cogs__gte">
                <Form.Label>COGS greater than...</Form.Label>
                <Form.Control type="text" placeholder="Enter COGS" />
              </Form.Group>

              <Button variant="primary" type="submit">
                Filter
              </Button>
              <Button
                variant="secondary"
                as={Link}
                to="/account/origin_report/create"
                className='ms-1'
              >Create</Button>
            </Form>
          </Container>
        </Col>
        <Col>
          <Row className="justify-content-md-center">
            {originReports.map((originReport, index) => (
              <ListItem key={index} originReport={originReport}/>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  )
}

export default CompanyOriginReport
