/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useState, useEffect, Fragment } from 'react'
import ListItem from '../components/ListItem'
import { Container, Row, Col, Form, Button } from 'react-bootstrap'

const ProductList = () => {
  const [products, setProducts] = useState([])

  useEffect(() => {
    getProducts()
  }, [])

  const getProducts = async () => {
    let response = ''
    try {
      response = await fetch('/api/product/get/')
    } catch (error) {
      alert('Server is not responding')
      return
    }
    const data = await response.json()
    setProducts(data)
  }

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const params = {}

    Object.keys(event.target).forEach(function (attr) {
      if (!isNaN(attr)) {
        params[event.target[attr].id] = event.target[attr].value
      }
    })
    const config = {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    }

    let query = '?'
    Object.keys(params).forEach(function (param) {
      if (params[param]) {
        query += param + '=' + params[param] + '&'
      }
    })

    let response = ''
    try {
      response = await fetch('/api/product/get/' + query, config)
    } catch (error) {
      alert('Server is not responding')
      return
    }
    const result = await response.json()
    setProducts(result)
  }

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
          <Row className='mt-2'>
              <p className='text-center'>Filters</p>
          </Row>
          <Container className="align-items-center py-2">
            <Fragment>
              <Form onSubmit={submitHandler}>
                <Form.Group className="mb-3" controlId="unique_identifier__icontains">
                  <Form.Label>Unique id contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter id" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="marketing_name__icontains">
                  <Form.Label>Public facing id contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter marketing name" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_cogs__lte">
                  <Form.Label>SCTR COGS less than...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR COGS" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_cogs__gte">
                  <Form.Label>SCTR COGS greater than...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR COGS" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="company__name__icontains">
                  <Form.Label>Company name contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter company name" />
                </Form.Group>

                <Button variant="primary" type="submit">
                  Filter
                </Button>
              </Form>
            </Fragment>
          </Container>
        </Col>
        <Col>
          <Row className="justify-content-md-center">
            {products.map((product, index) => (
              <ListItem key={index} product={product}/>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  )
}

export default ProductList
