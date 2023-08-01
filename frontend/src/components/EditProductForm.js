import React, { useContext, useEffect, useMemo, useState } from "react";
import { Button, Form} from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import { useNavigate, useParams } from "react-router-dom";
import FormContainer from "../utils/FormContainer";
import countryList from "react-select-country-list";


const EditProductForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  let { authTokens } = useContext(AuthContext)
  let { product_sku } = useParams()
  let [product, setProduct] = useState([])
  // If successfully editted, go to home page to prevent multiple editting
  let navigate = useNavigate()

  const options = useMemo(() => countryList().getData(), [])

  useEffect(() => {
    async function getProductInfo() {
      const config = {
        method: "GET",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": "Bearer " + authTokens.access
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
  
      const result = await response.json()
  
      if (response.status !== 200) {
        alert("Action not allowed")
        navigate("/")
      }
      else {
        setProduct(result)
      }
    }
    getProductInfo()
  }, [])

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

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

    // Config for PATCH request
    const config = {
      method: "PATCH",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + authTokens.access
      },
      body: JSON.stringify(data)
    }

    let response = ""
    try {
      response = await fetch("/api/product/patch_delete_retrieve/" + product_sku + "/", config)
    }
    catch (error) {
      alert("Server is not responding")
      return
    }

    const result = await response.json()

    if (response.status === 200) {
      alert("Successfully editted")
      navigate("/products/" + product_sku)
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
      navigate("/")
    }
  }

  return (
    <FormContainer>
      <Form onSubmit={submitHandler}>
        <Form.Group className="mb-3" controlId="sku_id">
          <Form.Label>Sku id</Form.Label>
          <Form.Control type="text" placeholder={product.sku_id} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="public_facing_id">
          <Form.Label>Public facing id</Form.Label>
          <Form.Control type="text" placeholder={product.public_facing_id} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="public_facing_name">
          <Form.Label>Public facing name</Form.Label>
          <Form.Control type="text" placeholder={product.public_facing_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="description">
          <Form.Label>Description</Form.Label>
          <Form.Control type="text" placeholder={product.description} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="sctr_date">
          <Form.Label>SCTR date</Form.Label>
          <Form.Control type="text" placeholder={product.sctr_date} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="sctr_cogs">
          <Form.Label>SCTR COGS</Form.Label>
          <Form.Control type="text" placeholder={product.sctr_cogs} />
        </Form.Group>
        
        <Form.Group className="mb-3" controlId="product_input_manufacturer">
          <Form.Label>Product input manufacturer</Form.Label>
          <Form.Control type="text" placeholder={product.product_input_manufacturer} />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Product type</Form.Label>
          <Form.Select aria-label="Select type" id="product_input_type">
            <option>{product.product_input_type}</option>
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
            <option>{product.cogs_coutry_recipients}</option>
            {options.map((option, i) => (
              <option key={option["value"]} value={option["value"]}>{option["label"]}</option>
            ))}
          </Form.Select>
        </Form.Group>

        <Button className="my-3" variant="primary" type="submit">
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditProductForm
