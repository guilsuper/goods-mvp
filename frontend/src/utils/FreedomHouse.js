/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

/**
 * return freedom house.org country report URL
 * @param  {string} countryName  country name of the desired report
 * @return {string}              country report link
 */
export function freedomHouseCountryReportURL (countryName) {
  const urlFriendlyCountryName = countryName.toLowerCase()
    .replaceAll(' ', '-')
    .replaceAll("'", '')
    .replaceAll('.', '')
  return 'https://freedomhouse.org/country/' + urlFriendlyCountryName + '/freedom-world/2023'
}
