/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Col, Row, Image } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { toReadable } from '../utils/Utilities'

const ListItem = ({ sctr }) => {
  ListItem.propTypes = {
    sctr: PropTypes.object
  }
  // If the SCTR wan't loaded yet
  if (!sctr.state) {
    return
  }

  // Renders sctr object as a column that contains 4 rows.
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={'/sctr/' + sctr.id}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        <Image src="/FreeWorldCertified-logo-192.png"/>
      </Row>
      <Row>
        {'SCTR unique identifier: ' + sctr.unique_identifier}
      </Row>
      <Row>
        {'SCTR facing name: ' + sctr.marketing_name}
      </Row>
      <Row>
        {'SCTR state: ' + toReadable(sctr.state)}
      </Row>
    </Col>
  )
}

export default ListItem
