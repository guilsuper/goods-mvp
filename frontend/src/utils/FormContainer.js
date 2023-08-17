/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { Container } from 'react-bootstrap'

function FormContainer (props) {
  FormContainer.propTypes = {
    children: PropTypes.any
  }

  const children = props.children
  return (
    <Container className="p-5 my-5 mx-auto w-75 rounded shadow">
      {children}
    </Container>
  )
};

export default FormContainer
