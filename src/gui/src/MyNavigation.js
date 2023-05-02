import { NavLink } from 'react-router-dom';
import "./MyNavigation.css"

const MyNavigation = () => {
  return (
    <nav>
      <ul>
        <li><NavLink exact to="/" activeClassName="active">Home</NavLink></li>
        <li><NavLink to="/search" activeClassName="active">Search</NavLink></li>
        <li><NavLink to="/trips" activeClassName="active">Trips</NavLink></li>
        <li id='log'><NavLink to="/login" activeClassName="active">LogIn</NavLink></li>
      </ul>
    </nav>
  );
}

export default MyNavigation;
