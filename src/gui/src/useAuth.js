import { useEffect, useState } from 'react';
import jwtDecode from 'jwt-decode';
import Cookies from 'js-cookie';

const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = Cookies.get('token');

    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        if (decodedToken.exp * 1000 > Date.now()) {
          setIsLoggedIn(true);
        }
      } catch (err) {
        console.error(err);
      }
    }
  }, []);

  return isLoggedIn;
};

export default useAuth;
