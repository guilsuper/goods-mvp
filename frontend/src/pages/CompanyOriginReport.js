/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import ListItem from '../components/ListItem'
import { Col, Container, Form, Row, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useSearchCompanyOriginReportsQuery } from '../api/OriginReport'
import LoadingComponent from '../components/LoadingComponent'

const CompanyOriginReport = () => {
  const [query, setQuery] = React.useState({})
  const { isLoading, isError, data: originReports, error } = useSearchCompanyOriginReportsQuery({ query })

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const params = {}

    Object.keys(event.target).forEach(function (attr) {
      if (!isNaN(attr)) {
        params[event.target[attr].id] = event.target[attr].value
      }
    })

    const q = {}
    Object.keys(params).forEach(function (param) {
      if (params[param]) {
        q[param] = params[param]
      }
    })
    setQuery(q)
  }

  let results
  if (isLoading) {
    results = (
      <LoadingComponent />
    )
  } else if (isError) {
    results = <Row><h2 className="text-center">An error has occurred: { error.message }</h2></Row>
  } else if (originReports.length === 0) {
    results = <Row><h2 className="text-center">No origin reports found...</h2></Row>
  } else {
    results = (
      <Row className="justify-content-md-center">
        {originReports.map((originReport, index) => (
          <ListItem key={index} originReport={originReport}/>
        ))}
      </Row>
    )
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
          {results}
        </Col>
      </Row>
    </Container>
  )
}

export default CompanyOriginReport
