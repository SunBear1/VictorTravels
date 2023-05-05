import React from 'react';
import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { UserContext } from './UserProvider';
import "./TripDetail.css"

const TripDetail = () => {
    const { itemInCart, addToCart } = useContext(UserContext);
    const isReserved = itemInCart();
    const { id } = useParams();
    //const [trip, setTrip] = useState(null);
    
    // TO DO USE EFFECT FOR TRIP FETCH
    const handleResravation = () => {
        addToCart(id);
        // POST TO BACKEND
    }; 

    const trip = {
        image: 'https://via.placeholder.com/400x300',
        name: 'Hotel A',
        location: 'Location A',
        description:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum at dui vel eros bibendum aliquam. Fusce vel dui sit amet risus auctor sagittis vel vel nunc. Suspendisse at libero vitae mauris pharetra tincidunt sed quis purus. Sed malesuada, leo in hendrerit hendrerit, metus elit sollicitudin elit, vitae tincidunt dolor lorem ut metus. Cras porttitor, dolor a dictum commodo, ipsum metus luctus lacus, vel facilisis arcu ex quis ipsum. Sed euismod ligula quis felis vehicula faucibus. Pellentesque mollis efficitur turpis id varius. Quisque condimentum, ipsum non rutrum convallis, velit ante aliquam velit, ac sagittis libero leo ut enim.',
        date: '2023-06-01 - 2023-06-10',
        diets: ['Breakfast', 'Dinner'],
        roomType: 'Standard',
        totalCost: 2000,
        pricePerPerson: 1000,
    };

    return (
        <div className="details-screen">
            <div className="details-header">
                <img src={trip.image} alt={trip.name} />
                <div className="details-header-text">
                    <h2>{trip.name}</h2>
                    <p>{trip.location}</p>
                </div>
            </div>
            <div className="details-body">
                <div className="details-column">
                    <h3>Inne terminy dla tej samej wycieczki:</h3>
                    <ul>
                        <li>2023-07-01 - 2023-07-10</li>
                        <li>2023-08-01 - 2023-08-10</li>
                    </ul>
                    <h3>Liczba osób:</h3>
                    <p>2 osoby (dorośli)</p>
                    <h3>Transport:</h3>
                    <p>Samolot</p>
                    <h3>Rodzaj diety:</h3>
                    <p>{trip.diets.join(', ')}</p>
                    <h3>Rodzaj pokoju:</h3>
                    <p>{trip.roomType}</p>
                    <h3>Cena łączna:</h3>
                    <p>{trip.totalCost} zł</p>
                    <h3>Cena za osobę:</h3>
                    <p>{trip.pricePerPerson} zł</p>
                    {!isReserved ? <button className="reserve-button" onClick={handleResravation}>Rezerwuj teraz</button>:<p>Zarezerwowany</p>}
                </div>
                <div className="details-column">
                    <h3>Opis hotelu:</h3>
                    <p>{trip.description}</p>
                    <h3>Lokalizacja:</h3>
                    <p>{trip.location}</p>
                </div>
            </div>
        </div>
    );
};

export default TripDetail;
