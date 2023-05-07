import { createContext, useState, useEffect } from 'react';
import jwtDecode from 'jwt-decode';
import Cookies from 'js-cookie';

export const UserContext = createContext();

const UserProvider = ({ children }) => {

  // Login function to update the username state
  const login = (token) => {
    const decodedToken = jwtDecode(token.replace("Bearer ", ""));
    Cookies.set('token', token);
    Cookies.set('username', decodedToken.login);
  };

  const getUsername = () => {
    return Cookies.get('username');
  }

  const getCart = () => {
    return JSON.parse(Cookies.get('cart') || '[]');
  }

  const getPurchasedTrips = () => {
    return JSON.parse(Cookies.get('purchasedTrips') || '[]');
  }


  // Logout function to clear the username state and the cart
  const logout = () => {
    Cookies.remove('token');
    Cookies.remove('username');
    Cookies.remove('purchasedTrips');
    Cookies.remove('cart');
    window.location.reload();
  };

  useEffect(() => {
    const timer = setInterval(() => {
      // Decrement timeLeft for each trip in the cart
      const cartItems = getCart();
      const cart = cartItems.map((trip) => ({
        ...trip,
        timeLeft: trip.timeLeft - 1,
      }));
      Cookies.set('cart', JSON.stringify(cart));
    }, 60000); // 1 minute interval

    // Clear the timer when component unmounts
    return () => clearInterval(timer);
  }, []);

  const addToPurchasedTrips = (trip) => {
    // Add the trip to the cart with initial timeLeft value of 30 minutes
    const trips = getPurchasedTrips();
    trips.push(trip);
    Cookies.set('purchasedTrips', JSON.stringify(trips));
  };

  const addToCart = (trip) => {
    // Add the trip to the cart with initial timeLeft value of 30 minutes
    const trips = getCart();

    const newTrip = {
      trip: trip,
      timeLeft: 60
    }
    trips.push(newTrip);
    Cookies.set('purchasedTrips', JSON.stringify(trips));
  };

  const removeFromCart = (tripId) => {
    // Remove the trip from the cart by filtering out the trip with matching id
    const trips = getCart();

    const newTrips = trips.filter((trip) => trip.id !== tripId)
    Cookies.set('purchasedTrips', JSON.stringify(newTrips));
  };

  const itemInCart = (id) => {
    const trips = getCart();
    if (trips.includes(id)) {
      return true;
    }
    return false;
  };

  return (
    <UserContext.Provider value={{ getUsername, getCart, getPurchasedTrips, login, logout, addToCart, removeFromCart, itemInCart, addToPurchasedTrips }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserProvider;
