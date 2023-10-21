/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Form } from 'react-bootstrap'
import PropTypes from 'prop-types'

import { useCountryListQuery } from '../api/CountryList'

const CountrySelect = ({ id, onChange, value }) => {
  CountrySelect.propTypes = {
    id: PropTypes.string,
    onChange: PropTypes.func,
    value: PropTypes.string
  }

  const { isLoading, isError, data: countryList, error } = useCountryListQuery({})

  if (isLoading) {
    return <span>Loading...</span>
  }

  if (isError) {
    return <span>An error has occurred: { error.message }</span>
  }

  return (
    <Form.Select
      aria-label="Select country"
      id={id}
      onChange={onChange}
      value={value}
    >
      {countryList.map((option, i) => (
        <option key={option.alpha_2} value={option.alpha_2}>{option.name}</option>
      ))}
    </Form.Select>
  )
}

export default CountrySelect
