/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { axios } from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const listCompanyProductManagers = async () => {
  const response = await axios.get('/pm/list/')
  return response.data
}

export const useListCompanyProductManagersQuery = () => {
  return useQuery({
    queryKey: ['company-product-managers'],
    queryFn: () => listCompanyProductManagers()
  })
}

const getProductManager = async ({ email }) => {
  const response = await axios.get(`/pm/patch_delete_retrieve/${email}/`)
  return response.data
}

export const useGetProductManagerQuery = ({ email }) => {
  return useQuery({
    queryKey: ['product-manager', email],
    queryFn: () => getProductManager({ email })
  })
}

const deleteProductManager = async ({ email }) => {
  const response = await axios.delete(`/pm/patch_delete_retrieve/${email}/`)
  return response.data
}

export const useDeleteProductManager = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (email) => deleteProductManager({ email }),
    onSuccess: (data, email, context) => {
      queryClient.invalidateQueries({ queryKey: ['product-manager', email] })
      queryClient.invalidateQueries({ queryKey: ['company-product-managers'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const createProductManager = async ({ pm }) => {
  const response = await axios.post(
    '/pm/create/',
    pm,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return response.data
}

export const useCreateProductManager = () => {
  return useMutation({
    mutationFn: (pm) => createProductManager({ pm }),
    onSuccess: (data, pm, context) => {
    },
    onError: (_, variables, context) => {
    }
  })
}

const editProductManager = async ({ email, update }) => {
  const response = await axios.patch(
    `/pm/patch_delete_retrieve/${email}/`, update
  )
  return response.data
}

export const useEditProductManager = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ email, update }) => editProductManager({ email, update }),
    onSuccess: (data, { email, update }, context) => {
      queryClient.invalidateQueries({ queryKey: ['product-manager', email] })
      queryClient.invalidateQueries({ queryKey: ['company-product-managers'] })
    },
    onError: (_, variables, context) => {
    }
  })
}
