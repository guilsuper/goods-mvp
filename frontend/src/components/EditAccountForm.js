import React, { useContext } from "react";
import { Button, Form} from "react-bootstrap";
import AuthContext from "../context/AuthContext";
import jwtDecode from "jwt-decode";
import { useNavigate } from "react-router-dom";
import FormContainer from "../utils/FormContainer";


const EditAccountForm = () => {

    let { authTokens, updateUser, user } = useContext(AuthContext)
    let navigate = useNavigate()

    const submitHandler = async (event) => {
        event.preventDefault();
        event.persist();

        let data = {}

        Object.keys(event.target).forEach(function(attr){
            if (!isNaN(attr)){
                if (event.target[attr].style){
                    event.target[attr].style = ""
                }
                if (event.target[attr].value !== ""){
                    data[event.target[attr].id] = event.target[attr].value
                }
            }
        })

        const config = {
            method: "PATCH",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + authTokens.access
            },
            body: JSON.stringify(data)
        }

        let user_id = jwtDecode(authTokens.access).user_id

        let response = ""
        try {
            response = await fetch("/api/patch_admin/" + user_id, config)
        }
        catch (error) {
            alert("Server is not working")
            return
        }

        const result = await response.json()

        if (response.status === 400) {
            let message = "Invalid input data:"
            for (const invalid_element in result){
                event.target[invalid_element].style = "border-color: red"

                message += "\n" + invalid_element + ": " + result[invalid_element]
            }
            alert(message)
        }
        else if (response.status === 401) {
            alert("Not authenticated")
          }
        else {
            alert("Successfully editted")
            updateUser()
            navigate("/account/info")
        }
    }

    return (
        <FormContainer>
            <Form onSubmit={submitHandler}>
                <Form.Group className="mb-3" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" placeholder={user.username} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter new password" />
                </Form.Group>

                <Form.Group className="mb-3" controlId="company_name">
                    <Form.Label>Company name</Form.Label>
                    <Form.Control type="text" placeholder={user.company_name} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="company_address">
                    <Form.Label>Company address</Form.Label>
                    <Form.Control type="text" placeholder={user.company_address} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="industry">
                    <Form.Label>Industry</Form.Label>
                    <Form.Control type="text" placeholder={user.industry} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="company_size">
                    <Form.Label>Company size</Form.Label>
                    <Form.Control type="text" placeholder={user.company_size} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="first_name">
                    <Form.Label>First name</Form.Label>
                    <Form.Control type="text" placeholder={user.first_name} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="last_name">
                    <Form.Label>Last name</Form.Label>
                    <Form.Control type="text" placeholder={user.last_name} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder={user.email} />
                </Form.Group>

                <Form.Group className="mb-3" controlId="phonenumber">
                    <Form.Label>Phone</Form.Label>
                    <Form.Control type="text" placeholder={user.phonenumber} />
                </Form.Group>

                <Button className="mb-3" variant="primary" type="submit">
                    Edit
                </Button>
            </Form>
        </FormContainer>
    )
}

export default EditAccountForm