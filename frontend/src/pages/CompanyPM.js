/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Col, Container, Row } from 'react-bootstrap'
import PMItem from '../components/PMItem'
import PMForm from '../components/PMForm'
import { useListCompanyProductManagersQuery } from '../api/ProductManager'
import LoadingComponent from '../components/LoadingComponent'

const CompanyPM = () => {
  const { isLoading, isError, data: pms, error } = useListCompanyProductManagersQuery()

  let results
  if (isLoading) {
    results = (
      <LoadingComponent />
    )
  } else if (isError) {
    results = <Row><h2 className="text-center">An error has occurred: { error.message }</h2></Row>
  } else if (pms.length === 0) {
    results = <Row><h2 className="text-center">No origin reports found...</h2></Row>
  } else {
    results = (
      <Row className="justify-content-md-center">
        {pms.map((PM, index) => (
          <PMItem key={index} PM={PM}/>
        ))}
      </Row>
    )
  }

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
            <PMForm />
        </Col>
        <Col>
          {results}
        </Col>
      </Row>
    </Container>
  )
}

export default CompanyPM
