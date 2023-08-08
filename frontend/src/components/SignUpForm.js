import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import { useNavigate } from "react-router-dom";
import SignUp from "./SignUpSteps/SignUp";
import CompanyVerification from "./SignUpSteps/CompanyVerification";


const SignUpForm = () => {
  
  let navigate = useNavigate()

  let [ state, setState ] = useState({
    step: 1,

    // Company administrator email
    email: "",
    password: "",
    company_website: "",
    company_name: "",

    company_jurisdiction: "",
    company_headquarters_physical_address: "",

    industry: "",
    company_size: "",
    company_phonenumber: "",
  })

  const submitHandler = async (event) => {
    event.preventDefault()
    event.persist()

    const formData = new FormData();

    // Add the text data from the state to the FormData
    for (const [key, value] of Object.entries(state)) {
      formData.append(key, value);
    }

    const config = {
      method: "POST",
      body: formData,
    }

    let response = ""
    try {
      response = await fetch("/api/admin_and_company/create/", config)
    }
    catch (error) {
      alert("Server is not working")
      return
    }

    const result = await response.json()

    if (response.status === 201) {
      alert("Successfully created. Check your email.")
      navigate("/")
    }
    else if (response.status === 400) {
      let message = "Invalid input data:"
      for (const invalid_element in result){
        message += "\n" + invalid_element + ": " + result[invalid_element]
      }
      alert(message)
    }
    else {
      alert("Not authenticated or permission denied")
    }
  }
  // proceed to the next step
  const nextStep = () => {
    setState(prevState => ({
      ...prevState,
      step: prevState.step + 1
    }))
  }

  const prevStep = () => {
    setState(prevState => ({
      ...prevState,
      step: prevState.step - 1
    }))
  }

  switch(state.step) {
    case 1:
      return (
        <Form onSubmit={submitHandler}>
          <SignUp
            nextStep={ nextStep }
            setState={ setState }
            state={ state }
          />
        </Form>
      )
    case 2:
      return (
        <Form onSubmit={submitHandler}>
          <CompanyVerification
            prevStep={ prevStep }
            nextStep={ nextStep }
            setState={ setState }
            state={ state }
          />
        </Form>
      )
    default: 
        // do nothing
  }
}

export default SignUpForm
