import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";


const AuthContext = createContext()


export default AuthContext


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

    let response = ""
    try {
        response = await fetch("/api/self/patch_delete_retrieve/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }
    let data = await response.json()

    localStorage.setItem("user", JSON.stringify(data))
    setUser(data)
  }

  let signInUser = async (event, tokens) => {

    const config = {
      method: "GET",
      headers: {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": "Bearer " + tokens.access
      },
    }

    let response = ""
    try {
        response = await fetch("/api/self/patch_delete_retrieve/", config)
    }
    catch (error) {
        alert("Server is not working")
        return
    }
    let data = await response.json()

    localStorage.setItem("authTokens", JSON.stringify(tokens))
    localStorage.setItem("user", JSON.stringify(data))

    setAuthTokens(tokens)
    setUser(data)

    navigate("/account/info")
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
    <AuthContext.Provider value={context_data}>
      {children}
    </AuthContext.Provider>
  )
}
