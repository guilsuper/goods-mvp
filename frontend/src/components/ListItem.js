/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Col, Row, Image } from 'react-bootstrap'
import { Link } from 'react-router-dom'

const ListItem = ({ sctr }) => {
  ListItem.propTypes = {
    sctr: PropTypes.object
  }
  // Renders sctr object as a column that contains 3 rows.
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={'/sctr/' + sctr.unique_identifier}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        <Image src="/FreeWorldCertified-logo-192.png"/>
      </Row>
      <Row>
        {'SCTR SKU id: ' + sctr.unique_identifier}
      </Row>
      <Row>
        {'SCTR facing name: ' + sctr.marketing_name}
      </Row>
    </Col>
  )
}

export default ListItem
