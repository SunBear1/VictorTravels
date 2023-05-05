import { createContext, useState, useEffect } from 'react';
import jwtDecode from 'jwt-decode';
import Cookies from 'js-cookie';

export const UserContext = createContext();

const UserProvider = ({ children }) => {
  const [username, setUsername] = useState('');
  const [cart, setCart] = useState([]);
  const [purchasedTrips, setPurchasedTrips] = useState([]);

  // Decode the JWT token and set the username
  const token = Cookies.get('token');
  if (token) {
    const decodedToken = jwtDecode(token);
    setUsername(decodedToken.username);
  }

  // Login function to update the username state
  const login = (token) => {
    const decodedToken = jwtDecode(token);
    setUsername(decodedToken.username);
    Cookies.set('token', token, { expires: 7, sameSite: 'strict' });
  };

  // Logout function to clear the username state and the cart
  const logout = () => {
    Cookies.remove('token');
    setUsername('');
    setCart([]);
  };

  useEffect(() => {
    const timer = setInterval(() => {
      // Decrement timeLeft for each trip in the cart
      setCart((prevCart) =>
        prevCart.map((trip) => ({
          ...trip,
          timeLeft: trip.timeLeft - 1,
        }))
      );
    }, 60000); // 1 minute interval

    // Clear the timer when component unmounts
    return () => clearInterval(timer);
  }, []);

  const addToPurchasedTrips = (trip) => {
    // Add the trip to the cart with initial timeLeft value of 30 minutes
    setPurchasedTrips((trips) => [...trips, trip]);
  };

  const addToCart = (trip) => {
    // Add the trip to the cart with initial timeLeft value of 30 minutes
    setCart((prevCart) => [...prevCart, { ...trip, timeLeft: 30 }]);
  };

  const removeFromCart = (tripId) => {
    // Remove the trip from the cart by filtering out the trip with matching id
    setCart((prevCart) => prevCart.filter((trip) => trip.id !== tripId));
  };

  const itemInCart = (id) => {
    if(cart.includes(id)){
        return true;
    }
    return false;
  };

  return (
    <UserContext.Provider value={{ username, cart, login, logout, addToCart, removeFromCart, itemInCart, addToPurchasedTrips }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;
