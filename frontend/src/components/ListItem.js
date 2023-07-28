import React from "react";
import { Col, Row, Image } from "react-bootstrap";


const ListItem = ({product}) => {
  return (
    <Col xs={3} className="border m-3 p-4 rounded">
        <Row>
          <Image src="logo192.png"/>
        </Row>
        <Row>
          {"Product SKU id: " + product.sku_id}
        </Row>
        <Row>
          {"Product facing name: " + product.public_facing_name}
        </Row>
    </Col>
  )
}

export default ListItem