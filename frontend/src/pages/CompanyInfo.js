/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect, useContext } from 'react'
import Container from 'react-bootstrap/Container'
import AuthContext from '../context/AuthContext'
import { Col, Row, Button } from 'react-bootstrap'
import { useParams, useNavigate, Link } from 'react-router-dom'
import ImageComponent from '../components/ImageComponent'

const CompanyInfo = () => {
  const { user, authTokens } = useContext(AuthContext)

  const { companyName } = useParams()
  const [company, setCompany] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getCompanyInfo () {
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
        response = await fetch('/api/company/patch_retrieve/' + companyName + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      let result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        result = { ...result, ...result.company }
        delete result.company
        setCompany(result)
      }
    }
    getCompanyInfo()
  }, [navigate, companyName])

  const isAdmin = () => {
    return user.groups.map(pair => (pair.name === 'Administrator'))
  }

  return (
    <Container>
      <h3 className='text-center'>Company information</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>Company website</p></Row>
        <Row><p>{company.website}</p></Row>

        <Row className='text-secondary'><p>Company name</p></Row>
        <Row><p>{company.name}</p></Row>

        <Row className='text-secondary'><p>Company jurisdiction</p></Row>
        <Row><p>{company.jurisdiction}</p></Row>

        {
          // If logo is set
          company.logo
            ? <ImageComponent src={company.logo} text={'Company logo'}/>
            : ' '
        }

        {
          isAdmin()
            ? <Row>
            <Col>
              <Button
                variant='primary'
                as={Link}
                to={'/account/company/edit/' + companyName}
            >Edit</Button>
            </Col>
          </Row>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default CompanyInfo
