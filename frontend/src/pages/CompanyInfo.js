/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect, useContext } from 'react'
import Container from 'react-bootstrap/Container'
import AuthContext from '../context/AuthContext'
import { Col, Row, Button } from 'react-bootstrap'
import { useParams, useNavigate, Link } from 'react-router-dom'

const CompanyInfo = () => {
  const { user } = useContext(AuthContext)

  const { companyName } = useParams()
  const [company, setCompany] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getCompanyInfo () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
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
        <Row><p>{company.company_website}</p></Row>

        <Row className='text-secondary'><p>Company name</p></Row>
        <Row><p>{company.company_name}</p></Row>

        <Row className='text-secondary'><p>Company jurisdiction</p></Row>
        <Row><p>{company.company_jurisdiction}</p></Row>

        <Row className='text-secondary'><p>Company headquarters physical address</p></Row>
        <Row><p>{company.company_headquarters_physical_address}</p></Row>

        <Row className='text-secondary'><p>Industry</p></Row>
        <Row><p>{company.industry}</p></Row>

        <Row className='text-secondary'><p>company_size</p></Row>
        <Row><p>{company.company_size}</p></Row>

        <Row className='text-secondary'><p>company_phonenumber</p></Row>
        <Row><p>{company.company_phonenumber}</p></Row>

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
