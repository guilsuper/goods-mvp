import React, { useContext, useEffect, useState } from 'react'
import { Row, Col, Container, Button } from 'react-bootstrap'
import { Link, useNavigate, useParams } from 'react-router-dom'
import AuthContext from '../context/AuthContext'


const PMAccountInfo = () => {
  let { user, authTokens } = useContext(AuthContext)
  let { pm_username } = useParams()
  let [pm, setPM] = useState([])
  let navigate = useNavigate()

  useEffect(() => {
    async function getPMInfo() {
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
        response = await fetch("/api/pm/patch_delete_retrieve/" + pm_username + "/" , config)
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
        setPM(result)
      }
    }
    getPMInfo()
  }, [])

  const isAllowedToChange = (user) => {
    if (user.group === "PM") {
      return false
    }
    return user.username === pm.boss
  }

  const deletePM = async (event) => {

    if (!window.confirm("Are you sure you want to permanently delete this PM?")){
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
        response = await fetch("/api/pm/patch_delete_retrieve/" + pm_username + "/", config)
    }
    catch (error) {
      alert("Server is not working")
      return
    }

    if (response.status === 204){
      alert("Successfully deleted")
      navigate("/account/pm")
    }
    else {
      alert("Wasn't deleted or permission denied")
    }
  }

  return (
    <Container>
      <h3 className="text-center">PM information</h3>
      <Col className="p-5 mb-5 mx-auto w-75 rounded shadow">
        <Row className="text-secondary"><p>Username</p></Row>
        <Row><p>{pm.username}</p></Row>
        <Row className="text-secondary"><p>User First Name</p></Row>
        <Row><p>{pm.first_name}</p></Row>
        <Row className="text-secondary"><p>User Last Name</p></Row>
        <Row><p>{pm.last_name}</p></Row>
        <Row className="text-secondary"><p>Email</p></Row>
        <Row><p>{pm.email}</p></Row>
        <Row className="text-secondary"><p>Phone</p></Row>
        <Row><p>{pm.phonenumber}</p></Row>
        <Row className="text-secondary"><p>Is account activated</p></Row>
        <Row><p>{pm.is_active ? "True" : "False"}</p></Row>

        <Row className="text-secondary"><p>Boss</p></Row>
        <Row><p>{pm.boss}</p></Row>

        {
          isAllowedToChange(user) ?
          <Row>
            <Col md={4}>
              <Button variant="primary" as={Link} to={"/account/pm/edit/" + pm.username}>Edit</Button>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Button variant="danger" onClick={deletePM}>Delete PM</Button>
            </Col>
          </Row> : " "
        }

      </Col>
    </Container>
  )
}

export default PMAccountInfo
