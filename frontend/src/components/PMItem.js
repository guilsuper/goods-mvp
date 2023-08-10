import React from "react";
import { Col, Row, Image } from "react-bootstrap";
import { Link } from "react-router-dom";


const PMItem = ({PM}) => {
  // Renders PM object as a column with 2 rows
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={"/account/pm/info/" + PM.email}
      style={{ color: "inherit", textDecoration: "inherit"}}
    >
      <Row>
        <Image src="/logo192.png"/>
      </Row>
      <Row>
        {"Email: " + PM.email}
      </Row>
    </Col>
  )
}

export default PMItem
