/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState } from 'react'
import { Navbar, Nav, NavLink, Button, ButtonGroup, Dropdown, DropdownButton } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'

const Header = () => {
  const { authTokens, logoutUser, user } = useContext(AuthContext)

  const [isToggle, setToggle] = useState(false)

  const updateToggle = () => {
    // Tracks if burger menu is toggled
    // If yes, dropdown menu should align start, else -- end
    // so it doesn't go outside the screen
    setToggle(!isToggle)
  }

  const authButton = () => {
    // If authorize display the dropdown menu, else -- sign in and sign up buttons
    if (authTokens === null) {
      return (
        <ButtonGroup className="me-3">
          <Button variant="dark" as={Link} to="/sign-in">Sign-in</Button>
          <Button variant="primary" as={Link} to="/sign-up">Sign-up</Button>
        </ButtonGroup>
      )
    } else {
      return (
        <DropdownButton
          as={ButtonGroup}
          variant="success"
          title={user.email}
          align={isToggle ? 'start' : 'end'}
          className="me-3"
        >
          <Dropdown.Item eventKey="accountInfo" href="/account/info">Profile settings</Dropdown.Item>
          <Dropdown.Item eventKey="signOut" onClick={logoutUser}>Signout</Dropdown.Item>
        </DropdownButton>
      )
    }
  }

  const isAdmin = () => {
    return user.groups.map(pair => (pair.name === 'Administrator'))
  }

  return (
    <Navbar
      collapseOnSelect
      expand="sm"
      bg="dark"
      data-bs-theme="dark"
      className="ps-3 mb-3"
    >
      <Navbar.Brand href="/"><img src="/FreeWorldCertified-logo.png"/>&nbsp;&nbsp;Free World Certified</Navbar.Brand>
      <Navbar.Toggle
        aria-controls="navbarScroll"
        data-bs-target="#navbarScroll"
        className="mt-1 mx-auto ms-1"
        onClick={updateToggle}
      />
      <Navbar.Collapse id="navbarScroll">
        <Nav>
          <NavLink eventKey="home" as={Link} to="/">Home</NavLink>
          <NavLink eventKey="sctr" as={Link} to="/sctr">SCTR</NavLink>
          <NavLink eventKey="about" as={Link} to="/about">About</NavLink>
          {user ? <NavLink eventKey="ourSCTR" as={Link} to="/account/sctr">Our SCTR</NavLink> : ' '}
          { user && isAdmin()
            ? <NavLink eventKey="accountPM" as={Link} to="/account/pm">
            Create PM
          </NavLink>
            : ' '}
        </Nav>
      </Navbar.Collapse>
      {authButton()}
    </Navbar>
  )
}

export default Header
