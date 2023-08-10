import React, { useContext, useEffect, useState } from 'react';
import { Col, Row, Container, Button } from 'react-bootstrap';
import { useNavigate, useParams, Link } from 'react-router-dom';
import AuthContext from '../context/AuthContext';


const ProductInfo = () => {
  let { user, authTokens } = useContext(AuthContext)
  let { product_sku } = useParams()
  let [ product, setProduct ] = useState([])

  let navigate = useNavigate()

  useEffect(() => {
    let navigate_effect = navigate
    async function getProductInfo() {
      const config = {
        method: "GET",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
        },
      }
  
      let response = ""
      try {
        response = await fetch("/api/product/patch_delete_retrieve/" + product_sku + "/" , config)
      }
      catch (error) {
        alert("Server is not working")
        return
      }
  
      let result = await response.json()

      if (response.status !== 200) {
        alert("Action not allowed")
        navigate_effect("/")
      }
      else {
        result = {...result, ...result.company}
        delete result.company
        setProduct(result)
      }
    }
    getProductInfo()
  }, [navigate, product_sku])

  const isAllowedToChange = (user) => {
    return (user.company.company_name === product.company_name)
  }

  const deleteProduct = async (event) => {

    if (!window.confirm("Are you sure you want to permanently delete this product?")){
      return
    }

    const config = {
      method: "DELETE",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + authTokens.access
      },
    }

    let response = ""
    try {
      response = await fetch("/api/product/patch_delete_retrieve/" + product_sku + "/", config)
    }
    catch (error) {
      alert("Server is not working")
      return
    }

    if (response.status === 204){
      alert("Successfully deleted")
      navigate("/account/products")
    }
    else {
      alert("Wasn't deleted or permission denied")
    }
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

        <Row className="text-secondary"><p>Product owner</p></Row>
        <Row><p>{product.company_name}</p></Row>

        {
          isAllowedToChange(user) ?
          <Row>
            <Col md={4}>
              <Button variant="primary" as={Link} to={"/account/products/edit/" + product.sku_id}>Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant="danger" onClick={deleteProduct}>Delete product</Button>
            </Col>
          </Row> : " "
        }

      </Col>
    </Container>
  )
}

export default ProductInfo
