/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { axios } from './axios'
import { useQuery } from '@tanstack/react-query'

const getCountryList = async () => {
  const response = await axios.get('/country/list/')
  const countryList = response.data
  countryList.sort((a, b) => { return a.name > b.name ? 1 : (a.name === b.name ? 0 : -1) })
  return countryList
}

export const useCountryListQuery = ({ ...options }) => {
  return useQuery({
    queryKey: ['countries'],
    queryFn: () => getCountryList(),
    staleTime: 5 * 60 * 1000,
    ...options
  })
}
