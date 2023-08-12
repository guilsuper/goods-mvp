/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext } from "react";
import { Button, Form} from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import FormContainer from "../utils/FormContainer";


const EditAccountForm = () => {
  // authTokens are for sending request to the backend
  // updateUser for updating current user localStorage
  // user is needed to display local storage information
  let { authTokens, updateUser, user } = useContext(AuthContext)
  // If successfully editted, go to home page to prevent multiple editting
  let navigate = useNavigate()

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
      response = await fetch("/api/self/patch_delete_retrieve/", config)
    }
    catch (error) {
      alert("Server is not responding")
      return
    }

    const result = await response.json()

    if (response.status === 200) {
      alert("Successfully editted")
      updateUser()
      navigate("/account/info")
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
    <FormContainer>
      <Form onSubmit={submitHandler}>
      <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" placeholder={user.email} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Enter new password" />
        </Form.Group>

        <Form.Group className="mb-3" controlId="first_name">
          <Form.Label>First name</Form.Label>
          <Form.Control type="text" placeholder={user.first_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="last_name">
          <Form.Label>Last name</Form.Label>
          <Form.Control type="text" placeholder={user.last_name} />
        </Form.Group>

        <Form.Group className="mb-3" controlId="phonenumber">
          <Form.Label>Phone</Form.Label>
          <Form.Control type="text" placeholder={user.phonenumber} />
        </Form.Group>

        <Button className="mb-3" variant="primary" type="submit">
          Edit
        </Button>
      </Form>
    </FormContainer>
  )
}

export default EditAccountForm
