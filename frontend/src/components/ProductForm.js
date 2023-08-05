import React, { useContext } from "react";
import { Button, Form } from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router";
import FormContainer from "../utils/FormContainer";


const ProductForm = () => {

  let {authTokens} = useContext(AuthContext)

  let navigate = useNavigate()

  const submitHandler = async (event) => {
    event.preventDefault();
    event.persist();

    let data = {}

    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        if (event.target[attr].style){
          event.target[attr].style = ""
        }
        data[event.target[attr].id] = event.target[attr].value
      }
    })

    const config = {
      method: "POST",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": "Bearer " + authTokens.access
      },
      body: JSON.stringify(data)
    }

    let response = ""
    try {
        response = await fetch("/api/product/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }

    const result = await response.json()

    if (response.status === 400) {
      let message = "Invalid input data:"
      for (const invalid_element in result){
        event.target[invalid_element].style = "border-color: red"

        message += "\n" + invalid_element + ": " + result[invalid_element]
      }
      alert(message)
    }
    else if (response.status === 401) {
      alert("Not authenticated")
    }
    else {
      alert("Successfully created")
      navigate("/account/info")
    }
  }

  return (
    <FormContainer>
        <Form onSubmit={submitHandler}>
          <Form.Group className="mb-3" controlId="sku_id">
            <Form.Label>Sku id</Form.Label>
            <Form.Control type="text" placeholder="Enter SKU id" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="public_facing_id">
            <Form.Label>Public facing id</Form.Label>
            <Form.Control type="text" placeholder="Enter Public facing id" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="public_facing_name">
            <Form.Label>Public facing name</Form.Label>
            <Form.Control type="text" placeholder="Enter Public name id" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control type="text" placeholder="Enter description" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="sctr_date">
            <Form.Label>SCTR date</Form.Label>
            <Form.Control type="text" placeholder="Enter SCTR date like YYYY-MM-DD" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="sctr_cogs">
            <Form.Label>SCTR COGS</Form.Label>
            <Form.Control type="text" placeholder="Enter SCTR COGS" />
          </Form.Group>
          
          <Form.Group className="mb-3" controlId="product_input_manufacturer">
            <Form.Label>Product input manufacturer</Form.Label>
            <Form.Control type="text" placeholder="Enter product input manufacturer" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="product_input_type">
            <Form.Label>Product input type</Form.Label>
            <Form.Control type="text" placeholder="Enter product input type" />
          </Form.Group>

          <Button className="mb-3" variant="primary" type="submit">
            Create product
          </Button>
        </Form>
      </FormContainer>
  )
}

export default ProductForm