/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { axios } from './axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

const searchOriginReports = async ({ query }) => {
  const queryString = Object.keys(query).length > 0 ? '?' + new URLSearchParams(query).toString() : ''
  const response = await axios.get(`/origin_report/get/${queryString}`)
  return response.data
}

export const useSearchOriginReportsQuery = ({ query }) => {
  return useQuery({
    queryKey: ['origin-reports', query],
    queryFn: () => searchOriginReports({ query })
  })
}

const searchCompanyOriginReports = async ({ query }) => {
  const queryString = Object.keys(query).length > 0 ? '?' + new URLSearchParams(query).toString() : ''
  const response = await axios.get(`/origin_report/get_by_company/${queryString}`)
  return response.data
}

export const useSearchCompanyOriginReportsQuery = ({ query }) => {
  return useQuery({
    queryKey: ['company-origin-reports', query],
    queryFn: () => searchCompanyOriginReports({ query })
  })
}

const getOriginReport = async ({ id }) => {
  const response = await axios.get(`/origin_report/delete_retrieve/${id}`)
  return response.data
}

export const useGetOriginReportQuery = ({ id, ...options }) => {
  return useQuery({
    queryKey: ['origin-report', id],
    queryFn: () => getOriginReport({ id }),
    ...options
  })
}

const deleteOriginReport = async ({ id }) => {
  const response = await axios.delete(`/origin_report/delete_retrieve/${id}/`)
  return response.data
}

export const useDeleteOriginReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id) => deleteOriginReport({ id }),
    onSuccess: (data, id, context) => {
      queryClient.invalidateQueries({ queryKey: ['origin-report', id] })
      queryClient.invalidateQueries({ queryKey: ['origin-reports'] })
      queryClient.invalidateQueries({ queryKey: ['company-origin-reports'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const moveToDraftOriginReport = async ({ id }) => {
  const response = await axios.patch(`/origin_report/to_draft/${id}/`)
  return response.data
}

export const useMoveToDraftOriginReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id) => moveToDraftOriginReport({ id }),
    onSuccess: (data, id, context) => {
      queryClient.invalidateQueries({ queryKey: ['origin-report', id] })
      queryClient.invalidateQueries({ queryKey: ['origin-reports'] })
      queryClient.invalidateQueries({ queryKey: ['company-origin-reports'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const switchVisibilityOriginReport = async ({ id }) => {
  const response = await axios.put(`/origin_report/switch_visibility/${id}/`)
  return response.data
}

export const useSwitchVisibilityOriginReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id) => switchVisibilityOriginReport({ id }),
    onSuccess: (data, id, context) => {
      queryClient.invalidateQueries({ queryKey: ['origin-report', id] })
      queryClient.invalidateQueries({ queryKey: ['origin-reports'] })
      queryClient.invalidateQueries({ queryKey: ['company-origin-reports'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const createOriginReport = async ({ parameters }) => {
  const response = await axios.post(
    '/origin_report/create/',
    parameters
  )
  return response.data
}

export const useCreateOriginReport = () => {
  return useMutation({
    mutationFn: (parameters) => createOriginReport({ parameters }),
    onSuccess: (data, id, context) => {
    }
  })
}

const createOriginReportDraft = async ({ parameters }) => {
  const response = await axios.post(
    '/origin_report/create_draft/',
    parameters
  )
  return response.data
}

export const useCreateOriginReportDraft = () => {
  return useMutation({
    mutationFn: (parameters) => createOriginReportDraft({ parameters }),
    onSuccess: (data, id, context) => {
    },
    onError: (_, variables, context) => {
    }
  })
}

const publishOriginReport = async ({ id }) => {
  const response = await axios.patch(`/origin_report/to_published/${id}/`)
  return response.data
}

export const usePublishOriginReport = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id) => publishOriginReport({ id }),
    onSuccess: (data, id, context) => {
      queryClient.invalidateQueries({ queryKey: ['origin-report', id] })
      queryClient.invalidateQueries({ queryKey: ['origin-reports'] })
      queryClient.invalidateQueries({ queryKey: ['company-origin-reports'] })
    },
    onError: (_, variables, context) => {
    }
  })
}

const editOriginReportDraft = async ({ id, parameters }) => {
  const response = await axios.patch(
    `/origin_report/patch/${id}/`,
    parameters
  )
  return response.data
}

export const useEditOriginReportDraft = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, parameters }) => editOriginReportDraft({ id, parameters }),
    onSuccess: (data, { id, parameters }, context) => {
      queryClient.invalidateQueries({ queryKey: ['origin-report', id] })
      queryClient.invalidateQueries({ queryKey: ['origin-reports'] })
      queryClient.invalidateQueries({ queryKey: ['company-origin-reports'] })
    },
    onError: (_, { id, parameters }, context) => {
    }
  })
}
