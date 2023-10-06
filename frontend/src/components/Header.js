/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React, { useContext, useState } from 'react'
import { Navbar, Nav, NavLink, Button, ButtonGroup, Dropdown, DropdownButton } from 'react-bootstrap'
import { Link } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import { useTranslation } from 'react-i18next'

const lngs = {
  en: { nativeName: 'English' },
  de: { nativeName: 'Deutsch' }
}

const Header = () => {
  const { authTokens, logoutUser, user } = useContext(AuthContext)

  const { t, i18n } = useTranslation()

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
          <Button variant="dark" as={Link} to="/sign-in">{ t('common.sign-in') }</Button>
          <Button variant="primary" as={Link} to="/sign-up">{ t('common.sign-up') }</Button>
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
          <Dropdown.Item eventKey="accountInfo" href="/account/info">{ t('navigation.profile-settings') }</Dropdown.Item>
          <Dropdown.Item eventKey="signOut" onClick={logoutUser}>{ t('common.sign-out') }</Dropdown.Item>

        </DropdownButton>
      )
    }
  }

  const isAdmin = () => {
    return user.groups.map(pair => (pair.name === 'Administrator'))
  }

  const languageButton = () => {
    return (
        <DropdownButton
          variant="success"
          title="Language"
          align='end'
          className="me-3"
        >
          {
            Object.keys(lngs).map((lng) => (
              <Dropdown.Item key={lng}
                             eventKey="changeLang{lng}"
                             onClick={ () => i18n.changeLanguage(lng) }
                             active={ i18n.resolvedLanguage === lng }
              >
                { lngs[lng].nativeName }
              </Dropdown.Item>
            ))
          }
        </DropdownButton>
    )
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
          <NavLink eventKey="home" as={Link} to="/">{ t('navigation.home') }</NavLink>
          <NavLink eventKey="originReport" as={Link} to="/origin_report">{ t('common.origin-report_other') }</NavLink>
          {user ? <NavLink eventKey="ourOriginReport" as={Link} to="/account/origin_report">{ t('navigation.our-origin-reports') }</NavLink> : ' '}
          { user && isAdmin()
            ? <NavLink eventKey="accountPM" as={Link} to="/account/pm">
                { t('navigation.create-product-owner') }
          </NavLink>
            : ' '}
        </Nav>
      </Navbar.Collapse>
      {authButton()}
      {languageButton()}
    </Navbar>
  )
}

export default Header
