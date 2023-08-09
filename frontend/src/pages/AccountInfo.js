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
        response = await fetch("/api/self/patch_delete_retrieve/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }

    if (response.status === 204){
        alert("Successfully deleted")
        logoutUser()
    }
    else {
      alert("Wasn't deleted or permission denied")
    }
  }

  const isAdmin = () => {
    let is_admin = false
    user.groups.map(pair => (pair.name === "Administrator" ? is_admin = true : " "))
    return is_admin
  }

  return (
    <Container>
      <h3 className="text-center">User information</h3>
      <Col className="p-5 mb-5 mx-auto w-75 rounded shadow">
        <Row className="text-secondary"><p>User First Name</p></Row>
        <Row><p>{user.first_name}</p></Row>
        <Row className="text-secondary"><p>User Last Name</p></Row>
        <Row><p>{user.last_name}</p></Row>
        <Row className="text-secondary"><p>Email</p></Row>
        <Row><p>{user.email}</p></Row>
        <Row className="text-secondary"><p>Phone</p></Row>
        <Row><p>{user.phonenumber}</p></Row>
        {
          isAdmin() ?
          <Row>
            <Col md={4}>
              <Button variant="primary" as={Link} to="/account/edit">Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant="danger" onClick={deleteAccount}>Delete account</Button>
            </Col>
          </Row> : " "
        }

      </Col>
    </Container>
  )
}

export default AccountInfo
