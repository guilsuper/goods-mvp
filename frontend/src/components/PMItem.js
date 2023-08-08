import React from "react";
import { Col, Row, Image } from "react-bootstrap";
import { Link } from "react-router-dom";


const PMItem = ({PM}) => {
  // Renders PM object as a column with 2 rows
  return (
    <Col
      xs={3}
      className="border m-3 p-4 rounded"
      as={Link} to={"/account/pm/info/" + PM.username}
      style={{ color: "inherit", textDecoration: "inherit"}}
    >
      <Row>
        <Image src="/logo192.png"/>
      </Row>
      <Row>
        {"Username: " + PM.username}
      </Row>
    </Col>
  )
}

export default PMItem
