/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import Container from 'react-bootstrap/Container'
import { Col, Row, Button } from 'react-bootstrap'
import { useParams, Link } from 'react-router-dom'
import ImageComponent from '../components/ImageComponent'
import { useGetCompanyQuery } from '../api/Company'
import { useUser } from '../lib/Auth'
import LoadingComponent from '../components/LoadingComponent'

const CompanyInfo = () => {
  const user = useUser({})

  const { companyName } = useParams()

  const { isLoading, isError, data: company, error } = useGetCompanyQuery({ name: companyName })

  const isAdmin = (user) => {
    if (user.isLoading || user.isError || !user.data) return false
    return user.data.groups.map(pair => (pair.name === 'Administrator'))
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
            isAdmin(user)
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
}

export default CompanyInfo
