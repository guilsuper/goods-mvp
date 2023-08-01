import React, {useState, useEffect, Fragment} from "react";
import ListItem from "../components/ListItem";
import { Container, Row, Col, Form, Button } from "react-bootstrap";


const ProductList = () => {

  let [products, setProducts] = useState([])

  useEffect(() => {
    getProducts()
  }, [])

  let getProducts = async () => {
    let response = ""
    try {
      response = await fetch("/api/product/get/")
    }
    catch (error) {
      alert("Server is not responding")
      return
    }
    let data = await response.json()
    setProducts(data)
  }

  let submitHandler = async (event) => {
    event.preventDefault();
    event.persist();

    let params = {}

    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        params[event.target[attr].id] = event.target[attr].value
      }
    })
    const config = {
      method: "GET",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
      },
    }

    let query = "?"
    Object.keys(params).forEach(function(param){
      if (params[param]) {
        query += param + "=" + params[param] + "&"
      }
    })

    let response = ""
    try {
      response = await fetch("/api/product/get/" + query, config)
    }
    catch (error) {
      alert("Server is not responding")
      return
    }
    const result = await response.json()
    setProducts(result)
  }

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
          <Row className="align-items-center mb-1">
            <Container>
              Filters
            </Container>
          </Row>
          <Container className="align-items-center py-4">
            <Fragment>
              <Form onSubmit={submitHandler}>
                <Form.Group className="mb-3" controlId="sku_id__icontains">
                  <Form.Label>Sku id contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SKU id" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="public_facing_id__icontains">
                  <Form.Label>Public facing id contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter Public facing id" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="public_facing_name__icontains">
                  <Form.Label>Public facing name contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter Public name id" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="description__icontains">
                  <Form.Label>Description contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter description" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_date__gt">
                  <Form.Label>SCTR date after...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR date like YYYY-MM-DD" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_date__lt">
                  <Form.Label>SCTR date before...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR date like YYYY-MM-DD" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_cogs__lte">
                  <Form.Label>SCTR COGS less than...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR COGS" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="sctr_cogs__gte">
                  <Form.Label>SCTR COGS greater than...</Form.Label>
                  <Form.Control type="text" placeholder="Enter SCTR COGS" />
                </Form.Group>
                
                <Form.Group className="mb-3" controlId="product_input_manufacturer__icontains">
                  <Form.Label>Product input manufacturer contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter product input manufacturer" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="product_input_type__icontains">
                  <Form.Label>Product input type contains...</Form.Label>
                  <Form.Control type="text" placeholder="Enter product input type" />
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
