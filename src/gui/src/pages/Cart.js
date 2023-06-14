import React, {useContext, useEffect, useState} from 'react';
import {UserContext} from '../UserProvider';
import {useNavigate} from 'react-router-dom';
import Cookies from "js-cookie";
import axios from 'axios';

function Cart() {
    const { getCart, removeFromCart, getPurchasedTrips, getTripFromCart } = useContext(UserContext);

    const navigate = useNavigate();
    const [trips, setTrips] = useState([]);
    const [tripsId, setTripsId] = useState(getCart());
    const [boughtTrips, setBoughtTrips] = useState([]);
    const [boughtTripsId, setBoughtTripsId] = useState(getPurchasedTrips());
    useEffect(
        () => {
            const fetchTrips = async () => {
                console.log(tripsId);
                const tripsData = await Promise.all(
                    tripsId.map(async trip => {
                        const response = await fetch(
                            `http://localhost:18000/api/v1/trips/trip/${trip.trip}`
                        );
                        const eventData = await response.json();
                        return eventData;
                    })
                );
                setTrips(tripsData);
                console.log(tripsData);
            };
            if (tripsId.length > 0) fetchTrips();
            else setTrips([]);
        },
        [tripsId]
    );

    useEffect(
        () => {
            const fetchBought = async () => {
                const tripsData = await Promise.all(
                    boughtTripsId.map(async trip => {
                        const response = await fetch(
                            `http://localhost:18000/api/v1/trips/trip/${trip.trip}`
                        );
                        const eventData = await response.json();
                        return eventData;
                    })
                );
                setBoughtTrips(tripsData);
            };
            fetchBought();
        },
        [boughtTripsId]
    );

    const handleRemove = id => {
        removeFromCart(id);
        setTripsId(getCart());
    };

    const handleBuy = async id => {
        const trip = getTripFromCart(id);
        const token = Cookies.get('token');
        console.log(token);
        const config = {
            headers: { Authorization: token },
        };
        try {
            const response = await axios.post(
                'http://localhost:18000/api/v1/purchases/' + trip.reservationId,
                null,
                config
            );
            console.log(response.data);
            navigate("/" + trip.trip + '/buy');
        } catch (error) {
            console.error(error);
        }

    };

    useEffect(() => {
        const intervalId = setInterval(() => {
            setTripsId(prevCountdowns => {
                return prevCountdowns
                    .filter(countdown => {
                        if (countdown.timeLeft === 0 || countdown.timeLeft < 0) {
                            handleRemove(countdown.trip);
                            return false; // remove this trip from the array
                        } else {
                            return true; // keep this trip in the array
                        }
                    })
                    .map(countdown => {
                        return { ...countdown, timeLeft: countdown.timeLeft - 1 };
                    });
            });
        }, 1000);
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className="flex justify-center">
            <div className="inline-flex items-center flex-col">
                <h1 className="mb-4 text-xl font-extrabold leading-none tracking-tight text-gray-900 md:text-xl lg:text-5xl dark:text-white">
                    Shopping cart
                </h1>
                {trips.length > 0
                    ? trips.map(trip => (
                        <div key={trip.id} className="mb-5">
                            <h2 className="text-slate-200">{trip.hotel.name}</h2>
                            <h3 className="text-slate-200 mb-1">{trip.localisation.country}</h3>
                            <img className="mb-1" src={trip.hotel.image} alt={trip.id}/>
                            <p>
                                <p className='text-slate-200'>Time
                                    left: {tripsId?.filter((obj) => obj.trip === trip.id)[0]?.timeLeft} seconds</p>
                            </p>
                            <div className="flex justify-around mt-2">
                                <button className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4"
                                        onClick={() => handleRemove(trip.id)}>Remove from Cart
                                </button>
                                <button className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4"
                                        onClick={() => handleBuy(trip.id)}>Buy Trip
                                </button>
                            </div>
                        </div>
                    ))
                    : <p className="tracking-widest text-gray-500 md:text-lg dark:text-gray-400 my-80">
                        Your cart is empty
                    </p>}
                <h2 className="text-lg font-medium text-gray-900 dark:text-white">
                    Trips bought:
                </h2>
                {boughtTrips.length !== 0
                    ? boughtTrips.map(trip => (
                        <div key={trip.id}>
                            <h2 className="text-slate-200">{trip.hotel.name}</h2>
                            <p>{trip.price}</p>
                        </div>
                    ))
                    : <p className="tracking-tight text-gray-500 md:text-lg dark:text-gray-400 mt-5">
                        No trips bought
                    </p>}
            </div>
        </div>
    );
}

export default Cart;
