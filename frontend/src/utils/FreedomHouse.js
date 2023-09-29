/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

/**
 * return freedom house.org country report URL
 * @param  {string} countryName  country name of the desired report
 * @return {string}              country report link
 */
export function freedomHouseCountryReportURL (countryName, freedomHouseURLCountryName) {
  return 'https://freedomhouse.org/country/' + freedomHouseURLCountryName + '/freedom-world/2023'
}
