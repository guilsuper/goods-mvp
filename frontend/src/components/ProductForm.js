import React, { useContext, useMemo } from "react";
import { Button, Form } from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router";

import countryList from 'react-select-country-list';


const ProductForm = () => {
  // authTokens are for sending request to the backend
  let {authTokens} = useContext(AuthContext)
  // all possible countries list
  const options = useMemo(() => countryList().getData(), [])

  let navigate = useNavigate()

  const submitHandler = async (event) => {

    let data = {}

    // set data value from the form
    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        if (event.target[attr].style){
            // Clear bg color
            event.target[attr].style = ""
        }
        if (event.target[attr].value !== ""){
            // Add key and value pair to data from form field
            data[event.target[attr].id] = event.target[attr].value
        }
      }
    })

    // Config for POST request
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
        response = await fetch("/api/product/create/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert("Successfully created")
      navigate("/account/products")
    }
    else if (response.status === 400) {
      let message = "Invalid input data:"
      for (const invalid_element in result){
        event.target[invalid_element].style = "border-color: red"

        message += "\n" + invalid_element + ": " + result[invalid_element]
      }
      alert(message)
    }
    else {
      alert("Not authenticated or permission denied")
    }
  }

  return (
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

      <Form.Group className="mb-3">
        <Form.Label>Product type</Form.Label>
        <Form.Select aria-label="Select type" id="product_input_type">
          <option>Select type</option>
          <option value="Convenience Goods">Convenience Goods</option>
          <option value="Raw Materials">Raw Materials</option>
          <option value="Software">Software</option>
          <option value="Hardware">Hardware</option>
          <option value="Consumer Electronics">Consumer Electronics</option>
          <option value="Cookware">Cookware</option>
          <option value="Appliances">Appliances</option>
          <option value="Homegoods">Homegoods</option>
          <option value="Clothing">Clothing</option>
          <option value="Jewelry">Jewelry</option>
          <option value="Art">Art</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Product country</Form.Label>
        <Form.Select aria-label="Select country" id="cogs_coutry_recipients">
          <option>Select country</option>
          {options.map((option, i) => (
            <option key={option["value"]} value={option["value"]}>{option["label"]}</option>
          ))}
        </Form.Select>
      </Form.Group>

      <Button className="my-3" variant="primary" type="submit">
        Create product
      </Button>
    </Form>
  )
}

export default ProductForm
