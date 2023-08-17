/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Col, Container, Row } from 'react-bootstrap'

const MainFooter = () => {
  return (
    <footer className="text-center text-white mt-auto" style={{ backgroundColor: 'rgba(0, 0, 0, 0.2)' }}>
      <Container className="p-2"></Container>
      <Container>
        <Row className="border-bottom mb-1 pb-1">
          <Col>
            <h4>Our story</h4>
          </Col>
          <Col>
            <h4>Contact</h4>
          </Col>
          <Col>
            <h4>Legal notices</h4>
          </Col>
        </Row>
        <Row className="py-2">
          <p className="text-center">© 2023 Company, Inc</p>
        </Row>
      </Container>
    </footer>
  )
}

export default MainFooter
