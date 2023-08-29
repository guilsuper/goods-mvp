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
            <h4><a href="/about" className="link-light link-offset-2 link-opacity-75 link-opacity-100-hover link-underline-opacity-0 link-underline-opacity-0-hover">Our Story</a></h4>
          </Col>
          <Col>
            <h4><a href="/terms" className="link-light link-offset-2 link-opacity-75 link-opacity-100-hover link-underline-opacity-0 link-underline-opacity-0-hover">Terms of Use</a></h4>
          </Col>
        </Row>
        <Row className="py-2">
            <p className="text-center">&copy; 2023 Free World Certified, P.B.C.</p>
        </Row>
      </Container>
    </footer>
  )
}

export default MainFooter
