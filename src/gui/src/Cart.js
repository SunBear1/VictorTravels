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
      console.log(tripsId);
      const tripsData = await Promise.all(
        tripsId.map(async (trip) => {
          const response = await fetch(`http://localhost:18000/api/v1/trips/trip/${trip.trip}`);
          const eventData = await response.json();
          return eventData;
        })
      );
      setTrips(tripsData);
      console.log(tripsData);
    };
    if(tripsId.length > 0) fetchTrips();
    else setTrips([]);
  }, [tripsId]);

  useEffect(() => {
    const fetchBought = async () => {
      const tripsData = await Promise.all(
        boughtTripsId.map(async (trip) => {
          const response = await fetch(`http://localhost:18000/api/v1/trips/trip/${trip.trip}`);
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
  const handleBuy = async(id) =>{
    removeFromCart(id);
    setTripsId(getCart());
  }

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTripsId(prevCountdowns => {
        return prevCountdowns.filter(countdown => {
          if (countdown.timeLeft === 0 || countdown.timeLeft < 0) {
            handleRemove(countdown.trip);
            return false; // remove this trip from the array
          } else {
            return true; // keep this trip in the array
          }
        }).map(countdown => {
          return { ...countdown, timeLeft: countdown.timeLeft - 1 };
        });
      });
    }, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <h2>Cart</h2>
      { trips.length > 0 ? 
        (trips.map((trip) => (
          <div key={trip.id}>
            <h2>{trip.hotel.name}</h2>
            <h3>{trip.localisation.country}</h3>
            <img src={trip.hotel.image} alt={trip.id} />
            <p>Time left: {tripsId?.filter(obj=> obj.trip === trip.id)[0]?.timeLeft} seconds</p>
            <button onClick={() => handleRemove(trip.id)}>Remove from Cart</button>
            
            <button onClick={() => handleBuy(trip.id)}>Buy Trip</button>
          </div>
        )))
        : 
        <p>Your cart is empty</p>
        }
        <h2>Trips bought</h2>
        {boughtTrips && boughtTrips.map((trip) => (
          <div key={trip.id}>
            <h2>{trip.hotel.name}</h2>
            <p>{trip.price}</p>
          </div>
        ))}
    </div>
  );
};

export default Cart;