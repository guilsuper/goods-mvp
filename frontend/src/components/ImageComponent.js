/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Row } from 'react-bootstrap'

const ImageComponent = ({ src, text }) => {
  ImageComponent.propTypes = {
    src: PropTypes.string,
    text: PropTypes.string
  }

  return (
    <>
      <Row className='text-secondary'><p>{text}</p></Row>
      <Row className='pb-3 w-25'>
        <img
          className='w-50 ms-3 img-thumbnail'
          src={src}
          // Means text or src. Eslint replaced it from "text ? text : src" statement
          alt={text || src}
        />
      </Row>
    </>
  )
}

export default ImageComponent
