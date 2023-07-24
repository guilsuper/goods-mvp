import React, { Fragment, useContext } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import AuthContext from "../context/AuthContext";
import FormContainer from "../utils/FormContainer";


const SignIn = () => {

  let {signInUser} = useContext(AuthContext)

  const submitHandler = async (event) => {
    event.preventDefault();
    event.persist();

    let data = {}

    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        event.target[attr].style = ""
        data[event.target[attr].id] = event.target[attr].value
      }
    })

    const config = {
      method: "POST",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    }

    let response = ""
    try {
        response = await fetch("/api/token/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }

    const tokens = await response.json()

    if (response.status === 401) {
      alert("Invalid input data")
    }
    else if (response.status === 500) {
      alert("Server is not working")
    }
    else {
      signInUser(event, tokens)
      alert("Successfully logged")
    }
  }

  return (
    <FormContainer>
        <Form onSubmit={submitHandler}>
          <Form.Group className="mb-3" controlId="username">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" />
          </Form.Group>

          <Form.Group className="mb-3" controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Enter password" />
          </Form.Group>

          <Button className="mb-3" variant="primary" type="submit">
            Sign In
          </Button>
        </Form>
    </FormContainer>
  )
}

export default SignIn