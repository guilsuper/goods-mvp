/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Row, Col, Container, Button } from 'react-bootstrap'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useGetProductManagerQuery, useDeleteProductManager } from '../api/ProductManager'
import { useUser } from '../lib/Auth'
import LoadingComponent from '../components/LoadingComponent'

const PMAccountInfo = () => {
  const user = useUser({})
  const { pmEmail } = useParams()
  const navigate = useNavigate()

  const { isLoading, isError, data: pm, error } = useGetProductManagerQuery({ email: pmEmail })

  const deleteProductManager = useDeleteProductManager()

  const isAllowedToChange = (user) => {
    if (!user.data) return false
    return (user.data?.company.name === pm.company.name)
  }

  const deletePM = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete this Product Manager?')) {
      return
    }

    deleteProductManager.mutate(pmEmail, {
      onSuccess: (data, variables, context) => {
        navigate('/account/pm')
      },
      onError: (_, variables, context) => {
        alert("Wasn't deleted or permission denied")
      }
    })
  }

  if (isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (isError) {
    return (
      <h2 className="text-center">An error has occurred: { error.message }</h2>
    )
  } else {
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
}

export default PMAccountInfo
