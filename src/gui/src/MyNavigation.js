import { NavLink, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import useAuth from './useAuth';
import { UserContext } from './UserProvider';
import "./MyNavigation.css"


const MyNavigation = () => {
  const isLoggedIn = useAuth();
  const { getUsername, logout } = useContext(UserContext);
  const navigate = useNavigate();
  const username = getUsername();


  const LogoutButton = () => {
    logout();
    navigate('/');
  };

  return (
    <nav>
      <ul>
        <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
        <li><NavLink to="/search" activeClassName="active">Search</NavLink></li>
        {isLoggedIn && <li><NavLink to="/cart" activeClassName="active">Cart</NavLink></li>}
        {isLoggedIn ? (<li className="logout">{username}<button onClick={LogoutButton}>Logout</button></li>):(<li id='log'><NavLink to="/login" activeClassName="active">LogIn</NavLink></li>)}
      </ul>
    </nav>
  );
}

export default MyNavigation;
