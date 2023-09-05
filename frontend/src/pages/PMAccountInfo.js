/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState } from 'react'
import { Row, Col, Container, Button } from 'react-bootstrap'
import { Link, useNavigate, useParams } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

const PMAccountInfo = () => {
  const { user, authTokens } = useContext(AuthContext)
  const { pmEmail } = useParams()
  const [pm, setPM] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    async function getPMInfo () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + authTokens.access
        }
      }

      let response = ''
      try {
        response = await fetch('/api/pm/patch_delete_retrieve/' + pmEmail + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        setPM(result)
      }
    }
    getPMInfo()
  }, [authTokens, navigate, pmEmail])

  const isAllowedToChange = (user) => {
    return (user.company.name === pm.company.name)
  }

  const deletePM = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete this Product Manager?')) {
      return
    }

    const config = {
      method: 'DELETE',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + authTokens.access
      }
    }

    let response = ''
    try {
      response = await fetch('/api/pm/patch_delete_retrieve/' + pmEmail + '/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 204) {
      alert('Successfully deleted')
      navigate('/account/pm')
    } else {
      alert("Wasn't deleted or permission denied")
    }
  }

  // If pm company wasn't loaded yet
  // When page renders, pm.company is undefined
  // And it is impossible to get pm.company.name for example
  if (!pm.company) {
    return
  }

  return (
    <Container>
      <h3 className="text-center">Product Manager information</h3>
      <Col className="p-5 mb-5 mx-auto w-75 rounded shadow">
        <Row className="text-secondary"><p>First Name</p></Row>
        <Row><p>{pm.first_name}</p></Row>
        <Row className="text-secondary"><p>Last Name</p></Row>
        <Row><p>{pm.last_name}</p></Row>
        <Row className="text-secondary"><p>Email</p></Row>
        <Row><p>{pm.email}</p></Row>
        <Row className="text-secondary"><p>Is account activated</p></Row>
        <Row><p>{pm.is_active ? 'True' : 'False'}</p></Row>

        {
          isAllowedToChange(user)
            ? <Row>
            <Col md={4}>
              <Button variant="primary" as={Link} to={'/account/pm/edit/' + pm.email}>Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant="danger" onClick={deletePM}>Delete</Button>
            </Col>
          </Row>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default PMAccountInfo
