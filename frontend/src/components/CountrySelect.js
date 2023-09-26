/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useMemo } from 'react'
import { Form } from 'react-bootstrap'
import PropTypes from 'prop-types'
import countryList from 'react-select-country-list'

const CountrySelect = ({ id, onChange, value, placeholder }) => {
  CountrySelect.propTypes = {
    id: PropTypes.string,
    onChange: PropTypes.func,
    value: PropTypes.string,
    placeholder: PropTypes.string
  }
  const options = useMemo(() => countryList().getData(), [])

  return (
    <Form.Select
      aria-label="Select country"
      id={id}
      placeholder={placeholder}
      onChange={onChange}
      value={value}
    >
      {options.map((option, i) => (
        <option key={option.value} value={option.value}>{option.label}</option>
      ))}
    </Form.Select>
  )
}

export default CountrySelect
