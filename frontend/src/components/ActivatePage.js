import React, { useEffect, useState } from 'react'
import { Container } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router'


const ActivatePage = () => {
    let {uidb64, token} = useParams()
    let [message, setMessage] = useState([])

    let navigate = useNavigate()

    useEffect(() => {
        activate()
    }, [])

    const activate = async () => {
        let response = await fetch("/api/activate/" + uidb64 + "/" + token)

        if (response.status === 200){
            setMessage("Successfully activated!")
        }
        else{
            navigate("/sign-un")
        }
    }

    return (
        <Container>
            <h2 className='text-center'>{message}</h2>
        </Container>
    )
}

export default ActivatePage