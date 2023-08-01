import React, { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router';


const ActivatePage = () => {
  let {uidb64, token} = useParams()
  let [message, setMessage] = useState([])
  let navigate = useNavigate()

  useEffect(() => {
    
    async function activate() {
      let response = ""
      try {
        response = await fetch("/api/activate/" + uidb64 + "/" + token)
      }
      catch (error) {
        alert("Server is not responding")
        return
      }

      if (response.status === 200){
        setMessage("Successfully activated!")
      }
      else{
        navigate("/sign-up")
      }
    }
    activate()
  }, [])

  return (
    <Container>
      <h2 className='text-center'>{message}</h2>
    </Container>
  )
}

export default ActivatePage
