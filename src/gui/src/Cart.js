import { useContext, useEffect, useState } from 'react';
import { UserContext } from './UserProvider';

const Cart = () => {
  const { getCart, removeFromCart, getPurchasedTrips } = useContext(UserContext);
  



  const [trips, setTrips] = useState([]);
  const [tripsId, setTripsId] = useState(getCart());
  const [boughtTrips, setBoughtTrips] = useState([]);
  const [boughtTripsId, setBoughtTripsId] = useState(getPurchasedTrips());

  useEffect(() => {
    const fetchTrips = async () => {
      const tripsData = await Promise.all(
        tripsId.map(async (id) => {
          const response = await fetch(`https://example.com/events/${id}`);
          const eventData = await response.json();
          return eventData;
        })
      );
      setTrips(tripsData);
    };
    fetchTrips();
  }, [tripsId]);

  useEffect(() => {
    const fetchBought = async () => {
      const tripsData = await Promise.all(
        boughtTripsId.map(async (id) => {
          const response = await fetch(`https://example.com/events/${id}`);
          const eventData = await response.json();
          return eventData;
        })
      );
      setBoughtTrips(tripsData);
    };
    fetchBought();
  }, [boughtTripsId]);

  const handleRemove = (id) =>{
    removeFromCart(id);
    setTripsId(getCart());
  }

  return (
    <div>
      <h2>Cart</h2>
      { trips.length > 0 ? 
        (trips.map((trip) => (
          <div key={trip.id}>
            <h2>{trip.title}</h2>
            <p>{trip.price}</p>
            <p>Time left: {trip.timeLeft} minutes</p>
            <button onClick={() => handleRemove(trip.id)}>Remove from Cart</button>
          </div>
        )))
        : 
        <p>Your cart is empty</p>
        }
        <h2>Trips bought</h2>
        {boughtTrips && boughtTrips.map((trip) => (
          <div key={trip.id}>
            <h2>{trip.title}</h2>
            <p>{trip.price}</p>
          </div>
        ))}
    </div>
  );
};

export default Cart;