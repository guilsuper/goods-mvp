/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'

/**
 * return a multiline
 * @param   {string} text       string to split into multiple paragraphs
 */
export function multilineTranslation (text) {
  const items = text.split('\n')
  return (
    <>
      { items.map((item, index) => <p key={index}>{item}</p>) }
    </>
  )
}
