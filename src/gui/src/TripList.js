import React from 'react';
import "./TripList.css"

const TripList = () => {
    const trips = [
        {
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel A',
            location: 'Location A',
            description: 'Description A',
            date: '2023-06-01 - 2023-06-10',
            diets: ['Breakfast', 'Dinner'],
            price: 1000,
        },
        {
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel B',
            location: 'Location B',
            description: 'Description B',
            date: '2023-07-01 - 2023-07-10',
            diets: ['All Inclusive'],
            price: 1500,
        },
        {
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel C',
            location: 'Location C',
            description: 'Description C',
            date: '2023-08-01 - 2023-08-10',
            diets: ['Breakfast', 'Lunch', 'Dinner'],
            price: 1200,
        },
    ];

    return (
        <div className="trip-list">
            <div className="search-bar">
                <form>
                    <label htmlFor="when">Kiedy?</label>
                    <input type="text" id="when" />

                    <label htmlFor="where">Dokąd?</label>
                    <input type="text" id="where" />

                    <label htmlFor="people">Liczba osób (uwzględniając przedziały wiekowe)</label>
                    <input type="text" id="people" />

                    <label htmlFor="from">Skąd?</label>
                    <input type="text" id="from" />

                    <label htmlFor="transport">Transport</label>
                    <select id="transport">
                        <option value="any">Dowolny</option>
                        <option value="own">Własny</option>
                        <option value="train">Pociąg</option>
                        <option value="plane">Samolot</option>
                    </select>

                    <button type="submit">Szukaj</button>
                </form>
            </div>

            <ul className="trip-items">
                {trips.map((trip, index) => (
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
                ))}
            </ul>
        </div>
    );
};

export default TripList;
