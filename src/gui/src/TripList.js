import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import "./TripList.css"

const TripList = () => {
    const [when, setWhen] = useState('');
    const [where, setWhere] = useState('');
    const [numPeople, setNumPeople] = useState('');
    const [transportType, setTransportType] = useState('');
    const [data, setData] = useState([]);



    const trips = [
        {
            id:1,
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel A',
            location: 'Location A',
            description: 'Description A',
            date: '2023-06-01 - 2023-06-10',
            diets: ['Breakfast', 'Dinner'],
            price: 1000,
        },
        {
            id:2,
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel B',
            location: 'Location B',
            description: 'Description B',
            date: '2023-07-01 - 2023-07-10',
            diets: ['All Inclusive'],
            price: 1500,
        },
        {
            id:3,
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel C',
            location: 'Location C',
            description: 'Description C',
            date: '2023-08-01 - 2023-08-10',
            diets: ['Breakfast', 'Lunch', 'Dinner'],
            price: 1200,
        },
    ];

    useEffect(() => {
        if(transportType === "Dowolny")setTransportType('');
        const fetchData = async () => {
          const response = await fetch(`https://example.com/api/data?when=${when}&where=${where}&numPeople=${numPeople}&transportType=${transportType}`);
          const json = await response.json();
          setData(json);
        };
        fetchData();
      }, [when, where, numPeople, transportType]);


    return (
        <div className="trip-list">
            <div className="search-bar">
                <form>
                <label>When:</label>
                <input type="text" value={when} onChange={(e) => setWhen(e.target.value)} />

                <label>Where:</label>
                <input type="text" value={where} onChange={(e) => setWhere(e.target.value)} />

                <label>Number of people:</label>
                <input type="text" value={numPeople} onChange={(e) => setNumPeople(e.target.value)} />

                <label>Transport type:</label>
                <select id="transport" onChange={(e) => setTransportType(e.target.value)} >
                    <option value="any">Dowolny</option>
                    <option value="own">Własny</option>
                    <option value="train">Pociąg</option>
                    <option value="plane">Samolot</option>
                </select>
                </form>
            </div>

            <ul className="trip-items">
                {trips.map((trip, index) => (
                    <Link to={"trip/" + trip.id}>
                    <li key={index} className="trip-item">
                        <img src={trip.image} alt={trip.name} className="trip-item__image" />
                        <div className="trip-item__details">
                            <h3 className="trip-item__name">{trip.name}</h3>
                            <p className="trip-item__location">{trip.location}</p>
                            <p className="trip-item__description">{trip.description}</p>
                            <p className="trip-item__date">{trip.date}</p>
                            <p className="trip-item__diets">Diety: {trip.diets.join(', ')}</p>
                            <p className="trip-item__price">Cena za osobę: {trip.price} zł</p>
                        </div>
                    </li>
                    </Link>
                ))}
            </ul>
        </div>
    );
};

export default TripList;
