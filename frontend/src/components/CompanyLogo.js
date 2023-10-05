/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Image, Row } from 'react-bootstrap'

const CompanyLogo = ({ companyLogo }) => {
  CompanyLogo.propTypes = {
    companyLogo: PropTypes.string
  }

  return (
    <>
      <Row className='text-secondary'><p>Company logo</p></Row>
      <Row className='pb-3 w-25'>
        <Image
            className='w-50 ms-3'
            src={companyLogo}
            thumbnail
        />
      </Row>
    </>
  )
}

export default CompanyLogo
