import { Navigate, Outlet } from "react-router-dom";


const PrivateRoute = () => {
    const authTokens = localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null

    return authTokens ? <Outlet /> : <Navigate to="/" />;
}

export default PrivateRoute
