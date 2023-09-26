/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useEffect, useState } from 'react'
import { Form } from 'react-bootstrap'
import PropTypes from 'prop-types'

const CountrySelect = ({ id, onChange, value }) => {
  CountrySelect.propTypes = {
    id: PropTypes.string,
    onChange: PropTypes.func,
    value: PropTypes.string
  }

  // Are constant values that represents all countries
  const [countries, setCountries] = useState([])

  useEffect(() => {
    async function getCountries () {
      let response = ''
      try {
        response = await fetch('/api/country/list/')

        if (response.status === 200) {
          const data = await response.json()
          setCountries(data)
        } else {
          alert('Unexpected response from server')
        }
      } catch (error) {
        alert('Server is not responding')
      }
    }
    getCountries()
  }, [setCountries])

  return (
    <Form.Select
      aria-label="Select country"
      id={id}
      onChange={onChange}
      value={value}
    >
      {countries.sort((a, b) => { return a.name > b.name ? 1 : (a.name === b.name ? 0 : -1) })
        .map((option, i) => (
        <option key={option.alpha_2} value={option.alpha_2}>{option.name}</option>
        ))}
    </Form.Select>
  )
}

export default CountrySelect
