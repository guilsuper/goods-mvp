/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import React from 'react'
import { Col, Row, Container, Button } from 'react-bootstrap'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { toReadable, calculateCOGS } from '../utils/Utilities'
import ReactCountryFlag from 'react-country-flag'
import ImageComponent from '../components/ImageComponent'
import { freedomHouseCountryReportURL } from '../utils/FreedomHouse'
import GetQRCode from '../components/QRCode'
import { useGetOriginReportQuery, useDeleteOriginReport, useMoveToDraftOriginReport, useSwitchVisibilityOriginReport } from '../api/OriginReport'
import { useUser } from '../lib/Auth'
import LoadingComponent from '../components/LoadingComponent'

const OriginReportInfo = () => {
  const user = useUser({})
  const { originReportIdentifier } = useParams()

  const qrcodeURL = window.location.href

  const navigate = useNavigate()

  const { isLoading, isError, data: originReport, error } = useGetOriginReportQuery({ id: originReportIdentifier })

  const isOwner = (user) => {
    // If not authorized
    if (user.isLoading || user.isError || !user.data) {
      return false
    }
    return (user.data?.company.name === originReport.company.name)
  }

  const deleteOriginReport = useDeleteOriginReport()

  const moveToDraftOriginReport = useMoveToDraftOriginReport()

  const switchVisibilityOriginReport = useSwitchVisibilityOriginReport()

  const actionDeleteOriginReport = async (event) => {
    if (!window.confirm('Are you sure you want to permanently delete this Origin Report?')) {
      return
    }

    deleteOriginReport.mutate(originReportIdentifier, {
      onSuccess: (data, variables, context) => {
        navigate('/account/origin_report')
      },
      onError: (_, variables, context) => {
        alert("Wasn't deleted or permission denied")
      }
    })
  }

  const moveToDraft = async (event) => {
    moveToDraftOriginReport.mutate(originReportIdentifier, {
      onSuccess: (data, variables, context) => {
        navigate('/account/origin_report')
      },
      onError: (_, variables, context) => {
        alert("Wasn't moved or permission denied")
      }
    })
  }
  const switchVisibility = async (event) => {
    switchVisibilityOriginReport.mutate(originReportIdentifier, {
      onSuccess: (data, variables, context) => {
        alert('Successfully switched visibility')
      },
      onError: (_, variables, context) => {
        alert("Visibility wasn't switched")
      }
    })
  }

  if (isLoading) {
    return (
      <LoadingComponent />
    )
  } else if (isError) {
    return (
      <h2 className="text-center">An error has occurred: { error.message }</h2>
    )
  } else {
    return (
      <Container>
        <h3 className='text-center'>Origin Report</h3>
        <Col className='p-5 mb-5 mx-auto w-75 rounded shadow'>
          {
            // If logo is set
            originReport.company.logo
              ? <ImageComponent src={originReport.company.logo} text={'Company logo'}/>
              : ' '
          }
          {
            // If thumbnail is set
            originReport.thumbnail
              ? <ImageComponent src={originReport.thumbnail_url} text={'Thumbnail'}/>
              : ' '
          }
          <Row className='text-secondary'><p>Identifier Type</p></Row>
          <Row><p>{originReport.unique_identifier_type}</p></Row>

          <Row className='text-secondary'><p>Identifier</p></Row>
          <Row><p>{originReport.unique_identifier}</p></Row>

          <Row className='text-secondary'><p>Short Description</p></Row>
          <Row><p>{originReport.short_description}</p></Row>

          {
            isOwner(user)
              ? <>
                  <Row className='text-secondary'><p>Is latest version</p></Row>
                  <Row><p>{originReport.is_latest_version ? 'True' : 'False'}</p></Row>
                  <Row className='text-secondary'><p>State</p></Row>
                  <Row><p>{toReadable(originReport.state)}</p></Row>
                  <Row className='text-secondary'><p>Version</p></Row>
                  <Row><p>{originReport.version}</p></Row>
                </>
              : ' '
          }
          {
            originReport.state === 'PUBLISHED'
              ? <>
                  <Row className='text-secondary'><p>QR Code</p></Row>
                  <Row><GetQRCode path={qrcodeURL} /></Row>
                </>
              : ' '
          }
          <p className='text-secondary'>COGS: {calculateCOGS(originReport.components)}%</p>

          <Row className='mt-4'>
            <Col className='ps-4'>
              <p className="text-center">Fraction of COGS</p>
            </Col>
            <Col className='ps-4'>
              <p className="text-center">Short Description</p>
            </Col>
            <Col className='ps-4'>
              <p className="text-center">Component type (Company Name & External SKU)</p>
            </Col>
            <Col className='ps-4'>
              <p className="text-center">Country of origin</p>
            </Col>
            <Col className='ps-4'>
              <p className="text-center">Country flag</p>
            </Col>
          </Row>

          {originReport.components.map((component, index) => (
            <Row key={`${component}~${index}`} className='mb-3 pt-2 ps-4 border rounded'>
              <Col><p>{component.fraction_cogs}</p></Col>

              <Col><p>{component.short_description}</p></Col>

              <Col>
                <Row><p>{toReadable(component.component_type)}</p></Row>
                <Row><p>{component.company_name}</p></Row>
                <Row><p>{component.external_sku}</p></Row>
              </Col>

              <Col>
                <p>
                  <a href={freedomHouseCountryReportURL(component.country_of_origin_info.name, component.country_of_origin_info.freedom_house_url_name)}>
                    {component.country_of_origin_info.name}
                  </a>
                </p>
              </Col>
              <Col className='d-flex align-items-center justify-content-center'>
                <ReactCountryFlag
                  countryCode={component.country_of_origin}
                  svg
                  style={{
                    width: '6.6em',
                    height: '5em',
                    border: '1px solid #dee2e6'
                  }}
                  title={component.country_of_origin_info.name}
                />
              </Col>
            </Row>
          ))}

          {
            isOwner(user)
              ? <Col className='w-25 mt-4'>
                  <Row className='mb-3'>
                    {
                      originReport.state === 'DRAFT'
                        ? <>
                            <Button
                              variant='primary'
                              as={Link}
                              to={'/account/origin_report/edit/' + originReport.id}
                            >Edit</Button>
                          </>
                        : <>
                            <Button variant='primary' onClick={moveToDraft}>Move to draft</Button>
                          </>
                    }
                  </Row>

                  <Row>
                    <Button variant='danger' onClick={actionDeleteOriginReport}>Delete Origin Report</Button>
                  </Row>

                  {
                    originReport.state !== 'DRAFT'
                      ? <Row className='mt-3'>
                          {
                            originReport.state === 'HIDDEN'
                              ? <>
                                  <Button variant='secondary' onClick={switchVisibility}>Unhide</Button>
                                </>
                              : <>
                                  <Button variant='secondary' onClick={switchVisibility}>Hide</Button>
                                </>
                          }
                        </Row>
                      : ' '
                  }

                </Col>
              : ' '
          }

        </Col>
      </Container>
    )
  }
}

export default OriginReportInfo
