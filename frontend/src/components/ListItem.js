/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Col, Row, Image } from 'react-bootstrap'
import { Link } from 'react-router-dom'

const ListItem = ({ product }) => {
  ListItem.propTypes = {
    product: PropTypes.object
  }
  // Renders product object as a column that contains 3 rows.
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={'/products/' + product.unique_identifier}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        <Image src="/logo192.png"/>
      </Row>
      <Row>
        {'Product SKU id: ' + product.unique_identifier}
      </Row>
      <Row>
        {'Product facing name: ' + product.marketing_name}
      </Row>
    </Col>
  )
}

export default ListItem
