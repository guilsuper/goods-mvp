/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Col, Row, Image } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { toReadable } from '../utils/Utilities'

const ListItem = ({ originReport }) => {
  ListItem.propTypes = {
    originReport: PropTypes.object
  }
  // If the OriginReport wasn't loaded yet
  if (!originReport.state) {
    return
  }

  // Renders originReport object as a column that contains 4 rows.
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={'/origin_report/' + originReport.id}
      style={{ color: 'inherit', textDecoration: 'inherit' }}
    >
      <Row>
        { originReport.thumbnail_url
          ? <Image src={originReport.thumbnail_url}/>
          : <Image src="/FreeWorldCertified-logo-192.png"/>
        }
      </Row>
      <Row>
        {'Identifier: ' + originReport.unique_identifier}
      </Row>
      <Row>
        {'Name: ' + originReport.short_description}
      </Row>
      <Row>
        {'State: ' + toReadable(originReport.state)}
      </Row>
    </Col>
  )
}

export default ListItem
