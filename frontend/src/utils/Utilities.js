/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

export function toReadable (macroCase) {
  // Split the string by underscores
  const parts = macroCase.split('_')

  // Capitalize the first letter of each part and convert the rest to lowercase
  const readableParts = parts.map(part => {
    return part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
  })

  // Join the parts back together with spaces
  return readableParts.join(' ')
}
