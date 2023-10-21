/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { Fragment } from 'react'
import ListItem from '../components/ListItem'
import { Container, Row, Col, Form, Button } from 'react-bootstrap'
import { useSearchOriginReportsQuery } from '../api/OriginReport'
import LoadingComponent from '../components/LoadingComponent'

const OriginReportList = () => {
  const [query, setQuery] = React.useState({})

  const { isLoading, isError, data: originReports, error } = useSearchOriginReportsQuery({ query })

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
            <Fragment>
              <Form onSubmit={submitHandler}>
                <Form.Group className="mb-3" controlId="unique_identifier__icontains">
                  <Form.Label>Identifier contains...</Form.Label>
                  <Form.Control type="text" placeholder="SKU" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="short_description__icontains">
                  <Form.Label>Short description...</Form.Label>
                  <Form.Control type="text" placeholder="short description" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="company__name__icontains">
                  <Form.Label>Company name contains...</Form.Label>
                  <Form.Control type="text" placeholder="company name" />
                </Form.Group>

                <Button variant="primary" type="submit">
                  Filter
                </Button>
              </Form>
            </Fragment>
          </Container>
        </Col>
        <Col>
          {results}
        </Col>
      </Row>
    </Container>
  )
}

export default OriginReportList
