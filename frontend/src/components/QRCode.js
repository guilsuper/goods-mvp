/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import PropTypes from 'prop-types'
import { QRCodeSVG } from 'qrcode.react'

function GetQRCode ({ path }) {
  GetQRCode.propTypes = {
    path: PropTypes.string
  }

  return (
    <QRCodeSVG
      value={path}
      size={128}
      bgColor={'#ffffff'}
      fgColor={'#00008b'}
      level={'H'}
      includeMargin={2}
      imageSettings={{
        src: '/FreeWorldCertified-logo-192.png',
        x: undefined,
        y: undefined,
        height: 24,
        width: 24,
        excavate: true
      }}
    />
  )
}

export default GetQRCode
