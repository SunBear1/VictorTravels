import { useContext, useState, useEffect } from 'react';
import { UserContext } from './UserProvider';

const TripTimer = ({ tripId }) => {
  const { cart, removeFromCart } = useContext(UserContext);
  const [cardNumber, setCardNumber] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [securityCode, setSecurityCode] = useState('');
  const [timeLeft, setTimeLeft] = useState(cart.find(trip => trip.id === tripId).timeLeft);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prevTimeLeft => prevTimeLeft - 1);
    }, 60000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (timeLeft === 0) {
      removeFromCart(tripId);
    }
  }, [timeLeft, removeFromCart, tripId]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    
  };

  return (
    <div>
        <h2>Payment Information</h2>
        <div>
            <label htmlFor="cardNumber">Card Number:</label>
            <input type="text" id="cardNumber" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} />
        </div>
        <div>
            <label htmlFor="expirationDate">Expiration Date:</label>
            <input type="text" id="expirationDate" value={expirationDate} onChange={(e) => setExpirationDate(e.target.value)} />
        </div>
        <div>
            <label htmlFor="securityCode">Security Code:</label>
            <input type="text" id="securityCode" value={securityCode} onChange={(e) => setSecurityCode(e.target.value)} />
        </div>
        <div>
            <button onClick={handleSubmit}>Purchase</button>
        </div>
        <p>Time left for trip {tripId}: {timeLeft} minutes</p>
    </div>
  );
};

export default TripTimer;