/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import Container from 'react-bootstrap/Container'
import { useTranslation } from 'react-i18next'
import { multilineTranslation } from '../utils/I18nUtils'

const OurMission = () => {
  const { t } = useTranslation()

  return (
    <Container className="align-items-center">
      <Container>
        <h3 className="text-center">{ t('common.our-mission') }</h3>
        <p style={{ textAlign: 'justify' }}>
          { multilineTranslation(t('our-mission.mission')) }
        </p>
      </Container>
    </Container>
  )
}

export default OurMission
