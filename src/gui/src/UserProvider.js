import {createContext, useEffect} from 'react';
import jwtDecode from 'jwt-decode';
import Cookies from 'js-cookie';

export const UserContext = createContext();

const UserProvider = ({children}) => {
    // Login function to update the username state
    const login = token => {
        const decodedToken = jwtDecode(token.replace('Bearer ', ''));
        Cookies.set('token', token);
        Cookies.set('username', decodedToken.login);
    };

    const getUsername = () => {
        return Cookies.get('username');
    };

    const getCart = () => {
        return JSON.parse(Cookies.get('cart') || '[]');
    };

    const getPurchasedTrips = () => {
        return JSON.parse(Cookies.get('purchasedTrips') || '[]');
    };

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
            const cart = cartItems
                .filter(trip => {
                    if (trip.timeLeft === 0 || trip.timeLeft < 0) {
                        return false;
                    } else {
                        return true;
                    }
                })
                .map(trip => {
                    return {...trip, timeLeft: trip.timeLeft - 1};
                });
            Cookies.set('cart', JSON.stringify(cart));
        }, 1000); // 1 minute interval

    // Clear the timer when component unmounts
        return () => clearInterval(timer);
  }, []);

    const addToPurchasedTrips = trip => {
        // Add the trip to the cart with initial timeLeft value of 30 minutes
        const trips = getPurchasedTrips();
        trips.push(trip);
        Cookies.set('purchasedTrips', JSON.stringify(trips));
    };

    const addToCart = (trip, reservationId) => {
        // Add the trip to the cart with initial timeLeft value of 30 minutes
        const trips = getCart();

        const newTrip = {
            trip,
            reservationId,
            timeLeft: 60,
        };
        trips.push(newTrip);
        Cookies.set('cart', JSON.stringify(trips));
    };

    const removeFromCart = tripId => {
        const trips = getCart();
        console.log(trips);
        const newTrips = trips.filter(trip => trip.trip !== tripId);
        console.log(newTrips);
        Cookies.set('cart', JSON.stringify(newTrips));
    };

    const getTripFromCart = tripId => {
        const trips = getCart();
        const trip_found = trips.find(trip => trip.trip === tripId);
        return trip_found;
    };

    const itemInCart = id => {
        const trips = getCart();
        return trips.some(obj => obj.trip === id);
    };

    return (
        <UserContext.Provider
            value={{
                getUsername,
                getCart,
                getPurchasedTrips,
                login,
                logout,
                addToCart,
                removeFromCart,
                itemInCart,
                addToPurchasedTrips,
                getTripFromCart
            }}
        >
            {children}
        </UserContext.Provider>
    );
};

export default UserProvider;
