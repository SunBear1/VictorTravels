import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import useAuth from './useAuth';
import Cookies from 'js-cookie';

function LoginRoute() {
    const token = Cookies.get('token');

    if (token) {
        return <Navigate to="/home" />;
    }
    return <Outlet/>;
  
}

export default LoginRoute;
