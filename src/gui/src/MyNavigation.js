import { NavLink, useNavigate } from 'react-router-dom';
import { useContext, useState } from 'react';
import useAuth from './useAuth';
import { UserContext } from './UserProvider';
import "./MyNavigation.css"


const MyNavigation = () => {
  const isLoggedIn = useAuth();
  const { username, logout } = useContext(UserContext);
  const navigate = useNavigate();

  const LogoutButton = () => {
    logout();
    navigate('/');
  };

  return (
    <nav>
      <ul>
        <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
        <li><NavLink to="/search" activeClassName="active">Search</NavLink></li>
        {isLoggedIn && <NavLink to="/cart" activeClassName="active">Cart</NavLink>}
        {isLoggedIn ? (<li>{username}<button onClick={LogoutButton}>Logout</button></li>):(<li id='log'><NavLink to="/login" activeClassName="active">LogIn</NavLink></li>)}
      </ul>
    </nav>
  );
}

export default MyNavigation;
