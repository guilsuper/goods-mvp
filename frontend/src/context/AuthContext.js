import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";


const AuthContext = createContext()


export default AuthContext;


export const AuthProvider = ({children}) => {

    let [authTokens, setAuthTokens] = useState( () =>
        localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null
    )
    let [user, setUser] = useState( () =>
        localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")) : null
    )

    const navigate = useNavigate()

    let updateUser = async () => {
        const config = {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + authTokens.access
            },
        }

        let response = await fetch("/api/get_current_user/", config)
        let data = await response.json()

        localStorage.setItem("user", JSON.stringify(data))
        setUser(data)
    }

    let signInUser = async (event, tokens) => {
        event.preventDefault();
        event.persist();

        const config = {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + tokens.access
            },
        }

        let response = await fetch("/api/get_current_user/", config)
        let data = await response.json()

        localStorage.setItem("authTokens", JSON.stringify(tokens))
        localStorage.setItem("user", JSON.stringify(data))

        setAuthTokens(tokens)
        setUser(data)

        navigate("/")
    }

    let logoutUser = () => {
        localStorage.removeItem("authTokens")
        localStorage.removeItem("user")

        setAuthTokens(null)
        setUser(null)

        navigate("/sign-in")
    }

    let context_data = {
        user: user,
        authTokens: authTokens,
        signInUser: signInUser,
        updateUser: updateUser,
        logoutUser: logoutUser,
    }

    return (
        <AuthContext.Provider value = {context_data}>
            {children}
        </AuthContext.Provider>
    )
}
