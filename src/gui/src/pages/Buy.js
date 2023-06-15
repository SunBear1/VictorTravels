import { useParams } from 'react-router-dom';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../UserProvider';
import { NavLink, useNavigate } from 'react-router-dom';
import Cookies from "js-cookie";
import axios from 'axios';

const Buy = () => {
  const { id } = useParams();
  const tripId = id;
  const navigate = useNavigate();
  const { addToPurchasedTrips, removeFromCart, itemInCart, getTripFromCart } = useContext(UserContext);
  const [cardNumber, setCardNumber] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [securityCode, setSecurityCode] = useState('');
  const [isGood, setIsGood] = useState(true);
  const [trip, setTrip] = useState(getTripFromCart(tripId));
  const isInCart = itemInCart(tripId);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTrip((prevTrip) => {
        const newTimeLeft = prevTrip.timeLeft - 1;
        if (newTimeLeft <= 0) {
          navigate("/");
          removeFromCart(prevTrip.trip);
          return { ...prevTrip, timeLeft: 0 };
        } else {
          return { ...prevTrip, timeLeft: newTimeLeft };
        }
      });
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);



  const handlePayment = async event => {
    event.preventDefault();
    const trip = getTripFromCart(id);
    const token = Cookies.get('token');
    console.log(trip);
    const config = {
      headers: { Authorization: token },
    };
    try {
      const response = await axios.post(
        'http://localhost:18000/api/v1/payments/' + trip.reservationId,
        null,
        config
      );
      console.log(response.data);
      addToPurchasedTrips(trip);
      removeFromCart(trip.trip);
      navigate("/");
    } catch (error) {
      console.error(error);
      setIsGood(false);
      if(error.status === 410)removeFromCart(trip.trip);
    }

  };


  return (
    <div>
      {isInCart
        ? <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <h2 className="mt-5 text-center text-2xl font-bold leading-9 tracking-tight text-slate-300">Payment Information TIME: {trip?.timeLeft}</h2>
          <div>
            <label
              htmlFor="cardNumber"
              className="block text-sm font-medium leading-6 text-slate-300"
            >Card Number:</label>
            <input
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              type="text"
              id="cardNumber"
              value={cardNumber}
              onChange={e => setCardNumber(e.target.value)}
            />
          </div>
          <div>
            <label
              htmlFor="expirationDate"
              className="block text-sm font-medium leading-6 text-slate-300"
            >Expiration Date:</label>
            <input
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              type="text"
              id="expirationDate"
              value={expirationDate}
              onChange={e => setExpirationDate(e.target.value)}
            />
          </div>
          <div>
            <label
              htmlFor="securityCode"
              className="block text-sm font-medium leading-6 text-slate-300"
            >Security Code:</label>
            <input
              className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"

              type="text"
              id="securityCode"
              value={securityCode}
              onChange={e => setSecurityCode(e.target.value)}
            />
          </div>
          <div>
            <button className="mt-5 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded" onClick={handlePayment}>Purchase</button>
          </div>
        </div>
        : <p>Trip is not in cart</p>}
        {!isGood && <div
                  className="flex mt-10 p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800"
                  role="alert"
              >
                <svg
                    aria-hidden="true"
                    className="flex-shrink-0 inline w-5 h-5 mr-3"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clipRule="evenodd"
                  />
                </svg>
                <span className="sr-only">Info</span>
                <div>
                  <span className="font-medium">Error!</span> Could not recive payment
                </div>
              </div>}
    </div>
  );
};

export default Buy;
