import React, {useState, useEffect, useContext} from 'react';
import { Col, Container, Row } from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import PMItem from '../components/PMItem';
import PMForm from '../components/PMForm';
import { useNavigate } from 'react-router-dom';


const CompanyPM = () => {

  let [PMs, setPM] = useState([])
  let {authTokens} = useContext(AuthContext)

  let navigate = useNavigate()

  useEffect(() => {
    async function getPMs() {
      const config = {
        method: "GET",
        headers: {
          "Authorization": "Bearer " + authTokens.access
        },
      }

      let response = ""
      try {
        response = await fetch("/api/pm/list/", config)
      }
      catch (error) {
        alert("Server is not responding")
        return
      }
      
      let data = await response.json()

      if (response.status !== 200) {
          alert("Permission denied")
          navigate("/")
      }
      setPM(data)
    }
    getPMs()
  }, [])

  return (
    <Container>
      <Row>
        <Col xs={3} className="my-4 px-4 py-2 rounded shadow">
            <PMForm />
        </Col>
        <Col>
          <Row className="justify-content-md-center">
            {PMs.map((PM, index) => (
              <PMItem key={index} PM={PM}/>
            ))}
          </Row>
        </Col>
      </Row>
    </Container>
  )
}

export default CompanyPM
