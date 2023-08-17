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
      as={Link} to={'/products/' + product.sku_id}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        <Image src="/logo192.png"/>
      </Row>
      <Row>
        {'Product SKU id: ' + product.sku_id}
      </Row>
      <Row>
        {'Product facing name: ' + product.public_facing_name}
      </Row>
    </Col>
  )
}

export default ListItem
