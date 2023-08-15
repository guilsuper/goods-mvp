/*
 * Copyright 2023 Free World Certified -- all rights reserved.
 */

import { Navigate, Outlet } from "react-router-dom";


const PrivateRoute = () => {
    const authTokens = localStorage.getItem("authTokens") ? JSON.parse(localStorage.getItem("authTokens")) : null

    return authTokens ? <Outlet /> : <Navigate to="/" />;
}

export default PrivateRoute
