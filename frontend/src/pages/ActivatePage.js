/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useEffect } from 'react'
import { Container } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router'
import { useActivateAccount } from '../api/Account'
import LoadingComponent from '../components/LoadingComponent'

const ActivatePage = () => {
  const { uidb64, token } = useParams()

  const navigate = useNavigate()

  const activateAccount = useActivateAccount()

  useEffect(() => {
    activateAccount.mutate({ uidb64, token }, {
      onSuccess: (data, variables, context) => {
      },
      onError: (_, variables, context) => {
        navigate('/sign-up')
      }
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []) // empty dependency array; ensures this only runs once

  if (activateAccount.isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (activateAccount.isError) {
    return (
      <h2 className="text-center">An error has occurred: { activateAccount.error.message }</h2>
    )
  } else {
    return (
      <Container>
        <h2 className='text-center'>Successfully activated!</h2>
      </Container>
    )
  }
}

export default ActivatePage
