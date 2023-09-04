/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useEffect, useState } from 'react'
import { Col, Row, Container, Button } from 'react-bootstrap'
import { useNavigate, useParams, Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

const ProductInfo = () => {
  const { user, authTokens } = useContext(AuthContext)
  const { productSku } = useParams()
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
        response = await fetch('/api/product/patch_delete_retrieve/' + productSku + '/', config)
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
  }, [navigate, productSku])

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
      response = await fetch('/api/product/patch_delete_retrieve/' + productSku + '/', config)
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
  // When page renders, product.company is undefined
  // And it is impossible to get product.company.name for example
  if (!product.company) {
    return
  }

  return (
    <Container>
      <h3 className="text-center">Product information</h3>
      <Col className="p-5 mb-5 mx-auto w-75 rounded shadow">
        <Row className="text-secondary"><p>SKU</p></Row>
        <Row><p>{product.sku_id}</p></Row>

        <Row className="text-secondary"><p>Public facing id</p></Row>
        <Row><p>{product.public_facing_id}</p></Row>

        <Row className="text-secondary"><p>Public facing name</p></Row>
        <Row><p>{product.public_facing_name}</p></Row>

        <Row className="text-secondary"><p>Description</p></Row>
        <Row><p>{product.description}</p></Row>

        <Row className="text-secondary"><p>SCTR date</p></Row>
        <Row><p>{product.sctr_date}</p></Row>

        <Row className="text-secondary"><p>SCTR COGS</p></Row>
        <Row><p>{product.sctr_cogs}</p></Row>

        <Row className="text-secondary"><p>Product input manufacturer</p></Row>
        <Row><p>{product.product_input_manufacturer}</p></Row>

        <Row className="text-secondary"><p>Product type</p></Row>
        <Row><p>{product.product_input_type}</p></Row>

        <Row className="text-secondary"><p>Product country</p></Row>
        <Row><p>{product.cogs_coutry_recipients}</p></Row>

        <Row className="text-secondary"><p>Product company</p></Row>
        <Row><p>{product.company.name}</p></Row>

        {
          isAllowedToChange(user)
            ? <Row>
            <Col md={4}>
              <Button variant="primary" as={Link} to={'/account/products/edit/' + product.sku_id}>Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant="danger" onClick={deleteProduct}>Delete product</Button>
            </Col>
          </Row>
            : ' '
        }

      </Col>
    </Container>
  )
}

export default ProductInfo
