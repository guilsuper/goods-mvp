/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import Container from 'react-bootstrap/Container'
import { useTranslation } from 'react-i18next'

const Home = () => {
  const { t } = useTranslation()
  return (
    <Container className="align-items-center">
      <Container>
        <h3 className="text-center">{ t('home.value') }</h3>
        <p style={{ textAlign: 'justify' }}>{ t('home.description') } </p>
      </Container>
    </Container>
  )
}

export default Home
