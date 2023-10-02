/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useEffect, useState, useRef } from 'react'
import { Container } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router'

const ActivatePage = () => {
  const { uidb64, token } = useParams()
  const [message, setMessage] = useState([])
  const activatedAlready = useRef(false)
  const navigate = useNavigate()

  useEffect(() => {
    async function activate () {
      if (!activatedAlready.current) {
        try {
          activatedAlready.current = true
          const response = await fetch('/api/activate/' + uidb64 + '/' + token + '/')
          if (response.status === 200) {
            setMessage('Successfully activated!')
          } else {
            navigate('/sign-up')
          }
        } catch (error) {
          alert('Server is not responding')
        }
      }
    }
    activate()
  }, [navigate, token, uidb64])

  return (
    <Container>
      <h2 className='text-center'>{message}</h2>
    </Container>
  )
}

export default ActivatePage
