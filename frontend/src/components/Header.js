import React, { useContext } from "react";
import { Navbar, Nav, Form, Button, ButtonGroup, Container, Dropdown } from "react-bootstrap";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";


const Header = () => {

    let {authTokens, logoutUser, user} = useContext(AuthContext)

    const authButton = () => {
        if (authTokens === null) {
            return (
                <ButtonGroup>
                    <Button variant="dark" as={Link} to="/sign-in">Sign-in</Button>
                    <Button variant="primary" as={Link} to="/sign-up">Sign-up</Button>
                </ButtonGroup>
            )
        } else {
            return (
              <Dropdown>
                <Dropdown.Toggle variant="success">
                  {user.username}
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item href="/account/info">Profile settings</Dropdown.Item>
                  <Dropdown.Item onClick={logoutUser}>Signout</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            )
        }
    }

    return (
        <>
            <Navbar bg="dark" data-bs-theme="dark">
                <Container>
                      <Navbar.Brand href="/">MVP</Navbar.Brand>
                      <Nav className="me-auto">
                          <Nav.Link href="/">Home</Nav.Link>
                          <Nav.Link href="/products">Products</Nav.Link>
                          <Nav.Link href="#services">Services</Nav.Link>
                          <Nav.Link href="#contact">Contact</Nav.Link>
                          <Nav.Link href="#about">About</Nav.Link>
                          {user ? <Nav.Link href="/account/create_product">{user.company_name} FWC Product</Nav.Link> : " "}
                      </Nav>

                      <Form inline="true" className="mx-3">
                          {authButton()}
                      </Form>
                </Container>
            </Navbar>
            <br />
        </>
    );
}

export default Header
