import './Navbar.css';
import {GiBoarTusks} from 'react-icons/gi';
import {NavLink, useNavigate} from 'react-router-dom';
import {useContext} from 'react';
import useAuth from '../../useAuth';
import {UserContext} from '../../UserProvider';

function Navbar() {
  const isLoggedIn = useAuth();
  const {getUsername, logout} = useContext(UserContext);
  const navigate = useNavigate();
  const username = getUsername();

  const LogoutButton = () => {
    logout();
    navigate('/');
  };
  return (
      <header className="bg-slate-800">
        <nav
            className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8"
            aria-label="Global"
        >
          <div className="flex lg:flex-1">
            <GiBoarTusks color="#e2e8f0" size={25}/>
            <div className="text-m font-semibold leading-6 text-slate-200 ml-1">
              Victor Travels
            </div>
          </div>
          <div className="hidden lg:flex lg:gap-x-12">
            <NavLink
                exact
                to="/"
                className="un link text-m font-semibold leading-6 text-slate-300 hover:text-cyan-300"
            >
              Homepage
            </NavLink>
            <NavLink
                exact
                to="/history"
                className="un link text-m font-semibold leading-6 text-slate-300 hover:text-cyan-300"
            >
              History
            </NavLink>
            <NavLink
                to="/search"
                className="un link text-m font-semibold leading-6 text-slate-300 hover:text-cyan-300"
            >
              Search
            </NavLink>
            {isLoggedIn &&
                <NavLink
                    to="/cart"
                    className="un link text-m font-semibold leading-6 text-slate-300 hover:text-cyan-300"
                >
                  Cart
                </NavLink>}
          </div>
          <div className="hidden lg:flex lg:flex-1 lg:justify-end">
            {isLoggedIn
                ? <div className="un text-m link font-semibold leading-6 text-slate-300 hover:text-cyan-300">
                  {username}
                  <div onClick={LogoutButton}>Logout</div>
                </div>
                : <NavLink
                    to="/login"
                    className="un text-m link font-semibold leading-6 text-slate-300 hover:text-cyan-300"
                >
                  Log in <span aria-hidden="true">&rarr;</span>
                </NavLink>}
          </div>
        </nav>
      </header>
  );
}

export default Navbar;
