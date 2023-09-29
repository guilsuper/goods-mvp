/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */
import React from 'react'
import OriginReportForm from '../components/OriginReportForm'
import { Container } from 'react-bootstrap'

const OriginReportCreate = () => {
  return (
    <Container className="my-4 px-4 py-2 rounded shadow">
      <OriginReportForm />
    </Container>
  )
}

export default OriginReportCreate
