/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { axios } from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const getCompany = async ({ name }) => {
  const response = await axios.get(`/company/patch_retrieve/${name}/`)
  return response.data
}

export const useGetCompanyQuery = ({ name }) => {
  return useQuery({
    queryKey: ['company', name],
    queryFn: () => getCompany({ name })
  })
}

const editCompany = async ({ name, update }) => {
  const response = await axios.patch(
    `/company/patch_retrieve/${name}/`, update
  )
  return response.data
}

export const useEditCompany = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ name, update }) => editCompany({ name, update }),
    onSuccess: (data, { name, update }, context) => {
      queryClient.invalidateQueries({ queryKey: ['company', name] })
      queryClient.invalidateQueries({ queryKey: ['authenticated-user'] })
    }
  })
}
