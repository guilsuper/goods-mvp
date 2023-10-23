/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { axios, axiosNoTokens } from './axios'
import { useMutation, useQueryClient } from '@tanstack/react-query'

const activateAccount = async ({ uidb64, token }) => {
  const response = await axios.get(`/activate/${uidb64}/${token}/`)
  return response.data
}

export const useActivateAccount = () => {
  return useMutation({
    mutationFn: ({ uidb64, token }) => activateAccount({ uidb64, token }),
    onSuccess: (data, { uidb64, token }, context) => {
    },
    onError: (_, { uidb64, token }, context) => {
    }
  })
}

const deleteAccount = async () => {
  const response = await axios.delete('/self/patch_delete_retrieve/')
  return response.data
}

export const useDeleteAccount = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => deleteAccount(),
    onSuccess: (data, variables, context) => {
      queryClient.invalidateQueries({ queryKey: ['authenticated-user'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const createAccount = async ({ formData }) => {
  const response = await axios.post(
    '/admin_and_company/create/',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return response.data
}

export const useCreateAccount = () => {
  return useMutation({
    mutationFn: (formData) => createAccount({ formData }),
    onSuccess: (data, formData, context) => {
    },
    onError: (_, variables, context) => {
    }
  })
}

const editAccount = async ({ update }) => {
  const response = await axios.patch(
    '/self/patch_delete_retrieve/', update
  )
  return response.data
}

export const useEditAccount = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (update) => editAccount({ update }),
    onSuccess: (data, update, context) => {
      queryClient.invalidateQueries({ queryKey: ['authenticated-user'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

export const signInUser = async ({ data }) => {
  const response = await axios.post(
    '/token/',
    data,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return response.data
}

export const getUserWTokens = async (tokens) => {
  const response = await axiosNoTokens.get('/self/patch_delete_retrieve/',
    { headers: { Authorization: `Bearer ${tokens.access}` } }
  )
  return response.data
}

export const getUser = async () => {
  const response = await axios.get('/self/patch_delete_retrieve/')
  return response.data
}
