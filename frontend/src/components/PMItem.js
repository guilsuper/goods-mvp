/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Col, Row, Image } from 'react-bootstrap'
import { Link } from 'react-router-dom'

const PMItem = ({ PM }) => {
  PMItem.propTypes = {
    PM: PropTypes.object
  }
  // Renders PM object as a column with 2 rows
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={'/account/pm/info/' + PM.email}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        <Image src="/FreeWorldCertified-logo-192.png"/>
      </Row>
      <Row>
        {'Email: ' + PM.email}
      </Row>
      { PM.first_name
        ? <Row>{'First Name: ' + PM.first_name}</Row>
        : ' '
      }
      { PM.last_name
        ? <Row>{'Last Name: ' + PM.last_name}</Row>
        : ' '
      }
    </Col>
  )
}

export default PMItem
