/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import Container from 'react-bootstrap/Container'
import { Col, Row, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import { useDeleteAccount } from '../api/Account'
import { useUser, useLogout } from '../lib/Auth'

const AccountInfo = () => {
  const user = useUser({})
  const logout = useLogout({})

  const deleteAccount = useDeleteAccount()

  const actionDeleteAccount = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete your account?')) {
      return
    }

    deleteAccount.mutate({}, {
      onSuccess: (data, variables, context) => {
        alert('Successfully deleted')
        logout.mutate({})
      },
      onError: (_, variables, context) => {
        alert('Wasn\'t deleted or permission denied')
      }
    })
  }

  const isAdmin = (user) => {
    if (user.isLoading || user.isError || !user.data) return false
    return user.data?.groups.map(pair => (pair.name === 'Administrator'))
  }

  return (
    <Container>
      <h3 className='text-center'>User information</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>User First Name</p></Row>
        <Row><p>{user.data?.first_name}</p></Row>
        <Row className='text-secondary'><p>User Last Name</p></Row>
        <Row><p>{user.data?.last_name}</p></Row>
        <Row className='text-secondary'><p>Email</p></Row>
        <Row><p>{user.data?.email}</p></Row>
        {
          isAdmin(user)
            ? <Row>
            <Col>
              <Button variant='primary' as={Link} to='/account/edit'>Edit</Button>
            </Col>
            <Col>
              <Button variant='danger' onClick={actionDeleteAccount}>Delete account</Button>
            </Col>
            <Col>
              <Button
                variant='primary'
                as={Link}
                to={'/account/company/info/' + user.data?.company.slug}
              >Company info</Button>
            </Col>
          </Row>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default AccountInfo
