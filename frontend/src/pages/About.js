/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import Container from 'react-bootstrap/Container'
import { useTranslation } from 'react-i18next'

const About = () => {
  const { t } = useTranslation()

  return (
    <Container className="align-items-center">
      <Container>
        <h3 className="text-center">{ t('common.about') }</h3>
          <p style={{ textAlign: 'justify' }}>...
        </p>
      </Container>
    </Container>
  )
}

export default About
