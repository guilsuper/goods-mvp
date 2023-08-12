/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, {useState, useEffect, useContext} from 'react';
import ProductForm from "../components/ProductForm";
import ListItem from "../components/ListItem";
import { Col, Container, Row } from "react-bootstrap";
import AuthContext from "../context/AuthContext";


const CompanyProducts = () => {

  let [products, setProducts] = useState([])
  let {user} = useContext(AuthContext)

  useEffect(() => {
    async function getProducts() {
      const company_name = user.company.company_name

      let response = ""
      try {
        response = await fetch("/api/product/get/?company__company_name=" + company_name)
      }
      catch (error) {
        alert("Server is not responding")
        return
      }
      let data = await response.json()

      setProducts(data)
    }
    getProducts()
  }, [user])

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
            <ProductForm />
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

export default CompanyProducts
