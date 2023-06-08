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
  const { getCart, removeFromCart, itemInCart, getTripFromCart } = useContext(UserContext);
  const [cardNumber, setCardNumber] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [securityCode, setSecurityCode] = useState('');
  const [trip, setTrip] = useState(getTripFromCart(tripId));
  const isInCart = itemInCart(tripId);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const newTrip = { ...trip, timeLeft: trip.timeLeft - 1 };
      if (newTrip.timeLeft === 0 || newTrip.timeLeft < 0)
      {
        navigate("/");
        removeFromCart(trip.trip);
      }
      else{ 
        setTrip(newTrip);
      }
    
  }, 1000);

  return () => clearInterval(intervalId);
}, []);


const handlePayment = async id => {
  const trip = getTripFromCart(id);
  const token = Cookies.get('token');
  console.log(token);
  const config = {
    headers: { Authorization: token },
  };
  try {
    const response = await axios.post(
      'http://localhost:18000/api/v1/payment/' + trip.reservationId,
      null,
      config
    );
    console.log(response.data);
    navigate("/");
  } catch (error) {
    console.error(error);
  }

};

const handleSubmit = async event => {
  event.preventDefault();
};

return (
  <div>
    {isInCart
      ? <div>
        <h2>Payment Information TIME: {trip[0]?.timeLeft}</h2>
        <div>
          <label htmlFor="cardNumber">Card Number:</label>
          <input
            type="text"
            id="cardNumber"
            value={cardNumber}
            onChange={e => setCardNumber(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="expirationDate">Expiration Date:</label>
          <input
            type="text"
            id="expirationDate"
            value={expirationDate}
            onChange={e => setExpirationDate(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="securityCode">Security Code:</label>
          <input
            type="text"
            id="securityCode"
            value={securityCode}
            onChange={e => setSecurityCode(e.target.value)}
          />
        </div>
        <div>
          <button onClick={handleSubmit}>Purchase</button>
        </div>
      </div>
      : <p>Trip is not in cart</p>}
  </div>
);
};

export default Buy;
