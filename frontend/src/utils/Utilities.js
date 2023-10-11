/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

/**
 * return user friendly word
 * @param   {string} macroCase  word in MACRO_CASE
 * @return  {string}            capitalized, lowercased with replaced '_' to ' '
 */
export function toReadable (macroCase) {
  // If empty or NULL -- return empty string
  if (!macroCase) {
    return ''
  }
  // Split the string by underscores
  const parts = macroCase.split('_')

  // Capitalize the first letter of each part and convert the rest to lowercase
  const readableParts = parts.map(part => {
    return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
  })

  // Join the parts back together with spaces
  return readableParts.join(' ')
}

/**
  * Quality of life feature, calculates all component COGS
 */
export const calculateCOGS = (components) => {
  const sum = components.reduce(function (prev, current) {
    return prev + +current.fraction_cogs
  }, 0)
  // If NaN
  if (!sum) {
    return 0
  }
  return sum
}
