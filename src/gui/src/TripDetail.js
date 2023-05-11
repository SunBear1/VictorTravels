import React from 'react';
import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext } from './UserProvider';
import "./TripDetail.css"
import axios from 'axios';
import CounterComp from './CounterComp';
import TransportBooking from './TransportBooking';
import useAuth from './useAuth';
import Cookies from 'js-cookie';

const TripDetail = () => {
    const isLoggedIn = useAuth();
    const { itemInCart, addToCart } = useContext(UserContext);
    const { id } = useParams();

    const isReserved = itemInCart(id);
    console.log(isReserved);
    const [trip, setTrip] = useState(null);

    const [selectedRoom, setSelectedRoom] = useState('');

    const [selectedDiet, setSelectedDiet] = useState('');
    const [adultCounter, setAdultCounter] = useState(0);
    const [childrenTo3yoCounter, setChildrenTo3yoCounter] = useState(0);
    const [childrenTo10yoCounter, setChildrenTo10yoCounter] = useState(0);
    const [childrenTo18yoCounter, setChildrenTo18yoCounter] = useState(0);

    const [transportFromCost, setTransportFromCost] = useState(null);
    const [transportFromId, setTransportFromId] = useState(null);
    const [transportToCost, setTransportToCost] = useState(null);
    const [transportToId, setTransportToId] = useState(null);
    const [ownTransportFrom, setOwnTransportFrom] = useState(true);
    const [ownTransportTo, setOwnTransportTo] = useState(true);

    const [numberOfDays, setNumberOfDays] = useState(null);

    const [finalPrice, setFinalPrice] = useState(null);



    useEffect(() => {
        axios.get(`http://localhost:18000/api/v1/trips/trip/${id}`)
            .then(response => {
                setTrip(response.data);
                console.log(response.data);
                const start = new Date(response.data.dateFrom);
                const end = new Date(response.data.dateTo);
                const daysDifference = Math.floor((end - start) / (1000 * 60 * 60 * 24));
                setNumberOfDays(daysDifference);
            })
            .catch(error => {
                console.error(error);
            });
    }, [id]);

    useEffect(() => {
        const sum = adultCounter + childrenTo3yoCounter + childrenTo10yoCounter + childrenTo18yoCounter;
        if (sum === 0) {
            setSelectedRoom(null);
        } else if (sum === 1) {
            const roomType = "studio"
            if (trip.hotel.rooms[roomType].available > 0) setSelectedRoom(roomType);
        } else if (sum === 2) {
            const roomType = "small"
            if (trip.hotel.rooms[roomType].available > 0) setSelectedRoom(roomType);
        } else if (sum === 3) {
            const roomType = "medium"
            if (trip.hotel.rooms[roomType].available > 0) setSelectedRoom(roomType);
        } else if (sum === 4) {
            const roomType = "large"
            if (trip.hotel.rooms[roomType].available > 0) setSelectedRoom(roomType);
        } else {
            const roomType = "apartment"
            if (trip.hotel.rooms[roomType].available > 0) setSelectedRoom(roomType);
        }
    }, [adultCounter, childrenTo10yoCounter, childrenTo3yoCounter, childrenTo18yoCounter]);


    useEffect(() => {
        const fetchPrice = async () => {
            try {
                const response = await axios.get('http://localhost:18000/api/v1/trips/price', {
                    params: {
                        adults: adultCounter,
                        kids_to_3yo: childrenTo3yoCounter,
                        kids_to_10yo: childrenTo10yoCounter,
                        kids_to_18yo: childrenTo18yoCounter,
                        number_of_days: numberOfDays,
                        room_cost: trip.hotel.rooms[selectedRoom].cost,
                        diet_cost: trip.hotel.diet[selectedDiet],
                        transport_to_cost: ownTransportTo ? null : transportToCost,
                        transport_from_cost: ownTransportFrom ? null : transportFromCost,
                    }
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                setFinalPrice(response.data);
                console.log(response.data);
            } catch (error) {
                console.error(error)

            }
        }
        fetchPrice();
    }, [ownTransportFrom, ownTransportTo, transportFromCost, transportToCost, selectedDiet, selectedRoom])

    const handleResravation = async (event) => {
        event.preventDefault();
        const sum = adultCounter + childrenTo3yoCounter + childrenTo10yoCounter + childrenTo18yoCounter;
        const token = Cookies.get('token');
        const data = { 
            hotel_id: trip.hotel.hotelId, 
            room_type: selectedRoom,
            connection_id_to: ownTransportTo ? null : transportToId,
            connection_id_from: ownTransportFrom ? null : transportToId,
            head_count:sum,
            price:finalPrice 
        };
        const config = {
            headers: { Authorization: token },
        };

        try {
            const response = await axios.post('http://localhost:18000/api/v1/reservations/' + trip.id, data, config);
            console.log(response.data);
            addToCart(trip.id);
        } catch (error) {
            console.error(error);
        }

    };

    const handleTransportFromBooking = (cost, id) => {
        setTransportFromCost(cost);
        setTransportFromId(id);
    };

    const handleTransportToBooking = (cost, id) => {
        setTransportToCost(cost);
        setTransportToId(id);
    };

    const handleParentInputChange = (value, parentId) => {
        switch (parentId) {
            case 1:
                setAdultCounter(value);
                break;
            case 2:
                setChildrenTo3yoCounter(value);
                break;
            case 3:
                setChildrenTo10yoCounter(value);
                break;
            case 4:
                setChildrenTo18yoCounter(value);
                break;
            default:
                break;
        }
    };


    return (
        <div>
            {!trip && <p>Loading</p>}
            {trip &&
                <div className="details-screen">
                    <div className="details-header">
                        <img src={trip.hotel.image} alt={trip.id} />
                        <div className="details-header-text">
                            <h2>{trip.localisation.country}</h2>
                            <p>{trip.hotel.name}</p>
                        </div>
                    </div>
                    <div className="details-body">
                        <div className="details-column">
                            <h3>Opis hotelu:</h3>
                            <p>{trip.hotel.description.map(value => <li>{value}</li>)}</p>
                            <h3>Lokalizacja:</h3>
                            <p>{trip.localisation.country}</p>
                            <p>{trip.localisation.region}</p>
                        </div>
                        <div className="details-column">
                            <h3>Liczba osób:</h3>
                            <div id='Osoby'>
                                <div><CounterComp getValue={handleParentInputChange} parentId={1} text="Dorośli" /></div>
                                <div><CounterComp getValue={handleParentInputChange} parentId={2} text="Dzieci do 3 lat" /></div>
                                <div><CounterComp getValue={handleParentInputChange} parentId={3} text="Dzieci do 10 lat" /></div>
                                <div><CounterComp getValue={handleParentInputChange} parentId={4} text="Dzieci do 18 lat" /></div>
                            </div>
                            <h3>Transport dojazdu z:</h3>
                            Własny
                            <input
                                type="checkbox"
                                checked={ownTransportFrom}
                                onChange={(e) => setOwnTransportFrom(e.target.checked)}
                            />
                            <TransportBooking locations={trip.from} disable={ownTransportFrom} getCost={handleTransportFromBooking} />

                            <h3>Transport powrotny do:</h3>
                            Własny
                            <input
                                type="checkbox"
                                checked={ownTransportTo}
                                onChange={(e) => { setOwnTransportTo(e.target.checked) }}
                            />
                            <TransportBooking locations={trip.to} disable={ownTransportTo} getCost={handleTransportToBooking} />
                            <h3>Rodzaj diety:</h3>
                            <div>
                                <label htmlFor="diet-select">Diet:</label>
                                <select id="diet-select" value={selectedDiet} onChange={(e) => setSelectedDiet(e.target.value)}>
                                    <option value="">-- Wybierz diete --</option>
                                    {Object.keys(trip.hotel.diet).map((diet) => (
                                        <option key={diet} value={diet}>
                                            {diet} - {trip.hotel.diet[diet]}zł
                                        </option>
                                    ))}
                                </select>
                                {selectedDiet && <p>Selected diet: {selectedDiet}</p>}
                            </div>
                            <h3>Rodzaje pokoju:</h3>

                            <div>
                                {selectedRoom && <p>Selected room: {selectedRoom}</p>}
                            </div>


                            <h3>Cena:</h3>

                            {!isReserved && (finalPrice ? <p>{finalPrice} zł</p> : <p>Loading</p>)}
                            {!isLoggedIn && <p>Zaloguj się by zarezerwować</p>}
                            {isLoggedIn &&  (!isReserved ? (selectedRoom && <button className="reserve-button" onClick={handleResravation}>Rezerwuj teraz</button>) : <p>Zarezerwowany</p>)}
                        </div>

                    </div>
                </div>
            }
        </div>
    );
};

export default TripDetail;
