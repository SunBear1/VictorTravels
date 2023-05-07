import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import "./TripList.css"

import LocationEnum from './LocationEnum';
import CounterComp from './CounterComp';
import DateRangePicker from './DateRangePicker';
import "./SearchComp.css"

const TripList = () => {

    const [transportType, setTransportType] = useState('');
    const [data, setData] = useState([]);

    const [startDate, setStartDate] = useState(null);
    const [endDate, setEndDate] = useState(null);

    const [selectedCountries, setSelectedCountries] = useState(null);
    const [showCheckboxes, setShowCheckboxes] = useState(true);

    const [adultCounter, setAdultCounter] = useState(null);
    const [child1Counter, setChild1Counter] = useState(null);
    const [child2Counter, setChild2Counter] = useState(null);
    const [child3Counter, setChild3Counter] = useState(null);

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const adult = searchParams.get('adult');
    const child1 = searchParams.get('child1');
    const child2 = searchParams.get('child2');
    const child3 = searchParams.get('child3');
    const date_start = searchParams.get('date-start');
    const date_end = searchParams.get('date-end');
    const locations = searchParams.get('locations');


    useEffect(() => {
        adult ? setAdultCounter(adult) : setAdultCounter(0);
        child1 ? setChild1Counter(child1) : setChild1Counter(0);
        child2 ? setChild2Counter(child2) : setChild2Counter(0);
        child3 ? setChild3Counter(child3) : setChild3Counter(0);
        date_start ? setStartDate(date_start) : setStartDate('');
        date_end ? setEndDate(date_end) : setEndDate('');
        locations ? setSelectedCountries(locations.split(',')) : setSelectedCountries([]);
    }, []);



    const handleLocationChange = (event) => {
        const { value, checked } = event.target;
        if (checked) {
            setSelectedCountries([...selectedCountries, value]);
        } else {
            setSelectedCountries(selectedCountries.filter((color) => color !== value));
        }
    };

    const handleParentInputChange = (value, parentId) => {
        switch (parentId) {
            case 1:
                setAdultCounter(value);
                break;
            case 2:
                setChild1Counter(value);
                break;
            case 3:
                setChild2Counter(value);
                break;
            case 4:
                setChild3Counter(value);
                break;
            default:
                break;
        }
    };

    const handleDateInputChange = (startDate, endDate) => {
        setStartDate(startDate);
        setEndDate(endDate);
    }

    const changeCheckboxes = (event) => {
        var checkboxes = document.getElementById("checkBoxes");
        console.log(checkboxes);
        if (showCheckboxes) {
            checkboxes.style.display = "block";
            setShowCheckboxes(false);
        } else {
            checkboxes.style.display = "none";
            setShowCheckboxes(true);
        }
    }


    const countriesCheckboxes = Object.keys(LocationEnum).map((location) => (
        <label key={location}>
            <input
                type="checkbox"
                value={LocationEnum[location]}
                checked={selectedCountries?.includes(LocationEnum[location])}
                onChange={handleLocationChange}
            />
            {LocationEnum[location]}
        </label>
    ));


    const trips = [
        {
            id: 1,
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel A',
            location: 'Location A',
            description: 'Description A',
            date: '2023-06-01 - 2023-06-10',
            diets: ['Breakfast', 'Dinner'],
            price: 1000,
        },
        {
            id: 2,
            image: 'https://via.placeholder.com/150x150',
            name: 'Hotel B',
            location: 'Location B',
            description: 'Description B',
            date: '2023-07-01 - 2023-07-10',
            diets: ['All Inclusive'],
            price: 1500,
        },
        {
            id: 3,
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
        if (transportType === "Dowolny") setTransportType('');
        const fetchData = async () => {

        };
        fetchData();
    }, [startDate, endDate, adultCounter, child1Counter, child2Counter, child3Counter, transportType]);


    return (
        <div className="trip-list">
            <div className="search-bar">
                <form>
                    <div>
                        <h1>Date Range Picker Examples</h1>
                        <DateRangePicker startDate={startDate} endDate={endDate} getValue={handleDateInputChange} />
                    </div>
                    <div id='Osoby'>
                        <div>{adultCounter>=0 && <CounterComp value={adultCounter} getValue={handleParentInputChange} parentId={1} text="Dorośli" />}</div>
                        <div><CounterComp value={child1Counter} getValue={handleParentInputChange} parentId={2} text="Dzieci 1" /></div>
                        <div><CounterComp value={child2Counter} getValue={handleParentInputChange} parentId={3} text="Dzieci 2" /></div>
                        <div><CounterComp value={child3Counter} getValue={handleParentInputChange} parentId={4} text="Dzieci 3" /></div>
                    </div>
                    <div id='Dokad'>
                        <div className='multipleSelection'>
                            <div className="selectBox" onClick={changeCheckboxes}>
                                <select>
                                    <option>Select locations</option>
                                </select>
                                <div className="overSelect"></div>
                            </div>
                            <div id='checkBoxes'>
                                {countriesCheckboxes}
                            </div>
                        </div>

                        <ul>
                            {selectedCountries?.map((option) => (
                                <div className='selectedLocationsList'><li key={option}>{option}</li><br /></div>
                            ))}
                        </ul>
                    </div>

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
