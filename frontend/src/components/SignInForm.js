import React, { useContext } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import AuthContext from "../context/AuthContext";
import FormContainer from "../utils/FormContainer";


const SignIn = () => {
  // Sets tokens and user information
  let {signInUser} = useContext(AuthContext)

  const submitHandler = async (event) => {
    event.preventDefault();
    event.persist();

    let data = {}

    // set data value from the form
    Object.keys(event.target).forEach(function(attr){
      if (!isNaN(attr)){
        data[event.target[attr].id] = event.target[attr].value
      }
    })

    // config for POST request
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

    if (response.status === 200) {
      signInUser(event, tokens)
      alert("Successfully logged")
    }
    else if (response.status === 401) {
      alert("Invalid input data")
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
          <Form.Control type="text" placeholder="Enter email" />
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
