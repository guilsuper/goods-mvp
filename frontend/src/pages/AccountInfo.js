import React, { useContext } from "react";
import Container from "react-bootstrap/Container";
import AuthContext from "../context/AuthContext";
import { Col, Row, Button } from "react-bootstrap";
import { Link } from "react-router-dom";


const AccountInfo = () => {

  let {user, logoutUser, authTokens} = useContext(AuthContext)

  const deleteAccount = async (event) => {

    if (!window.confirm("Are you sure you want to permanently delete your account?")){
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
        response = await fetch("/api/delete_current_user/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }

    const result = await response.json()

    if (result){
        alert("Successfully deleted")
        logoutUser()
    }
    else {
      alert("Wasn't deleted")
    }
  }

  return (
    <Container>
      <h3 className="text-center">User information</h3>
      <Col className="p-5 mb-5 mx-auto w-75 rounded shadow">
        <Row className="text-secondary"><p>Username</p></Row>
        <Row><p>{user.username}</p></Row>
        <Row className="text-secondary"><p>Company Name</p></Row>
        <Row><p>{user.company_name}</p></Row>
        <Row className="text-secondary"><p>Company Address</p></Row>
        <Row><p>{user.company_address}</p></Row>
        <Row className="text-secondary"><p>Industry</p></Row>
        <Row><p>{user.industry}</p></Row>
        <Row className="text-secondary"><p>Company Size</p></Row>
        <Row><p>{user.company_size}</p></Row>
        <Row className="text-secondary"><p>User First Name</p></Row>
        <Row><p>{user.first_name}</p></Row>
        <Row className="text-secondary"><p>User Last Name</p></Row>
        <Row><p>{user.last_name}</p></Row>
        <Row className="text-secondary"><p>Email</p></Row>
        <Row><p>{user.email}</p></Row>
        <Row className="text-secondary"><p>Phone</p></Row>
        <Row><p>{user.phonenumber}</p></Row>

        <Row>
          <Col md={4}>
            <Button variant="primary" as={Link} to="/account/edit">Edit</Button>
          </Col>
          <Col md={{ span: 4, offset: 4 }}>
            <Button variant="danger" onClick={deleteAccount}>Delete account</Button>
          </Col>
        </Row>

      </Col>
    </Container>
  )
}

export default AccountInfo