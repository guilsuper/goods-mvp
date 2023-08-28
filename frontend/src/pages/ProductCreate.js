/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */
import React from 'react'
import ProductForm from '../components/ProductForm'
import { Container } from 'react-bootstrap'

const ProductCreate = () => {
  return (
    <Container className="my-4 px-4 py-2 rounded shadow">
      <ProductForm />
    </Container>
  )
}

export default ProductCreate
