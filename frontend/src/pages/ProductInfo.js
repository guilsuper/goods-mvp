/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState, Fragment } from 'react'
import { Col, Row, Container, Button } from 'react-bootstrap'
import { useNavigate, useParams, Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

const ProductInfo = () => {
  const { user, authTokens } = useContext(AuthContext)
  const { productIdentifier } = useParams()
  const [product, setProduct] = useState([])

  const navigate = useNavigate()

  useEffect(() => {
    async function getProductInfo () {
      const config = {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      }

      let response = ''
      try {
        response = await fetch('/api/product/patch_delete_retrieve/' + productIdentifier + '/', config)
      } catch (error) {
        alert('Server is not working')
        return
      }

      const result = await response.json()

      if (response.status !== 200) {
        alert('Action not allowed')
        navigate('/')
      } else {
        setProduct(result)
      }
    }
    getProductInfo()
  }, [navigate, productIdentifier])

  const isAllowedToChange = (user) => {
    // If not authorized
    if (!user) {
      return false
    }
    return (user.company.name === product.company.name)
  }

  const deleteProduct = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete this product?')) {
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
      response = await fetch('/api/product/patch_delete_retrieve/' + productIdentifier + '/', config)
    } catch (error) {
      alert('Server is not working')
      return
    }

    if (response.status === 204) {
      alert('Successfully deleted')
      navigate('/account/products')
    } else {
      alert("Wasn't deleted or permission denied")
    }
  }

  // If product company wasn't loaded yet
  // When page renders, product.company is undefiend
  // And it is imposible to get product.company.name for example
  if (!product.company) {
    return
  }

  return (
    <Container>
      <h3 className='text-center'>Product information</h3>
      <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
        <Row className='text-secondary'><p>Unique identifier</p></Row>
        <Row><p>{product.unique_identifier}</p></Row>

        <Row className='text-secondary'><p>Unique dentifier type</p></Row>
        <Row><p>{product.unique_identifier_type}</p></Row>

        <Row className='text-secondary'><p>Marketing name</p></Row>
        <Row><p>{product.marketing_name}</p></Row>

        {product.components.map((component, index) => (
        <Fragment key={`${component}~${index}`}>
          <Container className='my-4 p-3 border rounded'>
            <Row className='text-secondary'><p>Marketing name</p></Row>
            <Row><p>{component.marketing_name}</p></Row>

            <Row className='text-secondary'><p>Fraction COGS</p></Row>
            <Row><p>{component.fraction_cogs}</p></Row>

            <Row className='text-secondary'><p>Component type</p></Row>
            <Row><p>{component.component_type}</p></Row>

            {
              (component.component_type === 'Made In-House')
                ? <>
                  <Row className='text-secondary'><p>Country of origin</p></Row>
                  <Row><p>{component.country_of_origin}</p></Row>
                </>
                : <>
                  <Row className='text-secondary'><p>External SKU</p></Row>
                  <Row><p>{component.external_sku}</p></Row>
                </>
            }
          </Container>
        </Fragment>
        ))}

        {
          isAllowedToChange(user)
            ? <Row>
            <Col md={4}>
              <Button variant='primary' as={Link} to={'/account/products/edit/' + product.unique_identifier}>Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant='danger' onClick={deleteProduct}>Delete product</Button>
            </Col>
          </Row>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default ProductInfo
