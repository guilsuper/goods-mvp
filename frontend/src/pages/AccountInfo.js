/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext } from 'react'
import Container from 'react-bootstrap/Container'
import AuthContext from '../context/AuthContext'
import { Col, Row, Button } from 'react-bootstrap'
import { Link } from 'react-router-dom'

const AccountInfo = () => {
  const { user, logoutUser, authTokens } = useContext(AuthContext)
  const deleteAccount = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete your account?')) {
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
      response = await fetch('/api/self/patch_delete_retrieve/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 204) {
      alert('Successfully deleted')
      logoutUser()
    } else {
      alert('Wasn\'t deleted or permission denied')
    }
  }

  const isAdmin = () => {
    return user.groups.map(pair => (pair.name === 'Administrator'))
  }

  return (
    <Container>
      <h3 className='text-center'>User information</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>User First Name</p></Row>
        <Row><p>{user.first_name}</p></Row>
        <Row className='text-secondary'><p>User Last Name</p></Row>
        <Row><p>{user.last_name}</p></Row>
        <Row className='text-secondary'><p>Email</p></Row>
        <Row><p>{user.email}</p></Row>
        <Row className='text-secondary'><p>Phone</p></Row>
        <Row><p>{user.phonenumber}</p></Row>
        {
          isAdmin()
            ? <Row>
            <Col>
              <Button variant='primary' as={Link} to='/account/edit'>Edit</Button>
            </Col>
            <Col>
              <Button variant='danger' onClick={deleteAccount}>Delete account</Button>
            </Col>
            <Col>
              <Button
                variant='primary'
                as={Link}
                to={'/account/company/info/' + user.company.slug}
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
