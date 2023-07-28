import React from "react";
import { Container } from "react-bootstrap";

function FormContainer(props) { 
  return (
    <Container className="p-5 my-5 mx-auto w-75 rounded shadow">
        {props.children}
    </Container>
  );
};

export default FormContainer;