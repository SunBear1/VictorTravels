import './App.css';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import LocationEnum from './LocationEnum';
import CounterComp from './CounterComp';
import DateRangePicker from './DateRangePicker';

import axios from 'axios';
import "./SearchComp.css"



function SearchComp() {

  const navigate = useNavigate();


  const [trips, setTrips] = useState([]);
  const [transportType, setTransportType] = useState('');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const [selectedCountries, setSelectedCountries] = useState([]);
  const [showCheckboxes, setShowCheckboxes] = useState(true);

  const [adultCounter, setAdultCounter] = useState(0);
  const [childrenTo3yoCounter, setChildrenTo3yoCounter] = useState(0);
  const [childrenTo10yoCounter, setChildrenTo10yoCounter] = useState(0);
  const [childrenTo18yoCounter, setChildrenTo18yoCounter] = useState(0);

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

  const handleDateInputChange = (startDate, endDate) => {
    console.log(startDate);
    console.log(endDate);
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
        checked={selectedCountries.includes(LocationEnum[location])}
        onChange={handleLocationChange}
      />
      {LocationEnum[location]}
    </label>
  ));

  const handleSubmit = async (event) => {
    event.preventDefault();
    const options = { month: '2-digit', day: '2-digit', year: 'numeric' };
    const formattedStartDate = startDate.toLocaleDateString('en-US', options);
    const formattedEndDate = endDate.toLocaleDateString('en-US', options);

    const encodedList = selectedCountries.join(',');
    navigate(`/trips?adult=${adultCounter}&child1=${childrenTo3yoCounter}&child2=${childrenTo10yoCounter}&child3=${childrenTo18yoCounter}&date-start=${formattedStartDate}&date-end=${formattedEndDate}&locations=${encodedList}`);
  }


  const handleSubmit1 = async (event) => {
    if(transportType === "Dowolny")transportType = null;
    event.preventDefault();
    try {
      const response = await axios.get('http://localhost:18000/api/v1/trips', {
        params:{
          adults: adultCounter,
          kids_to_3yo: childrenTo3yoCounter,
          kids_to_10yo: childrenTo10yoCounter,
          kids_to_18yo: childrenTo18yoCounter,
          date_from: startDate,
          date_to: endDate,
          arrival_region: selectedCountries
        }
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      setTrips(response.data);
      console.log(response.data);
    } catch (error) {
      console.error(error)
      
    }
  }

  return (
    <div className="Search">

      <div>
        <h1>Date Range for Trip</h1>
        <DateRangePicker getValue={handleDateInputChange} />
      </div>
      <div id='Osoby'>
        <div><CounterComp getValue={handleParentInputChange} parentId={1} text="Dorośli" /></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={2} text="Dzieci do 3 lat" /></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={3} text="Dzieci do 10 lat" /></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={4} text="Dzieci do 18 lat" /></div>
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
          {selectedCountries.map((option) => (
            <div className='selectedLocationsList'><li key={option}>{option}</li><br /></div>
          ))}
        </ul>
      </div>

      <div>
        <label id="transport">Transport type:</label>
        <select onChange={(e) => setTransportType(e.target.value)} >
          <option value="any">Dowolny</option>
          <option value="own">Własny</option>
          <option value="train">Pociąg</option>
          <option value="plane">Samolot</option>
        </select>
      </div>
      <br />
      <button onClick={handleSubmit1}>Szukaj</button>

      <ul className="trip-items">
        {trips.map((trip, index) => (
          <Link to={"trip/" + trip.id}>
            <li key={index} className="trip-item">
              <img src={trip.hotel.image} alt={trip.id} className="trip-item__image" />
              <div className="trip-item__details">
                <h3 className="trip-item__name">{trip.localisation.country} {trip.hotel.name}</h3>
                <p className="trip-item__location">{trip.localisation.country.region}</p>
                <p className="trip-item__description">{trip.hotel.description.map(value => <li>{value}</li>)}</p>
                <p className="trip-item__date">OD : {trip.dateFrom}</p>
                <p className="trip-item__date">DO : {trip.dateTo}</p>
                <p className="trip-item__diets">Diety: {Object.keys(trip.hotel.diet).map(key => <li>{key}: {trip.hotel.diet[key]}</li>)}</p>
                <p className="trip-item__price">Cena za osobę: {trip.price} zł</p>
              </div>
            </li>
          </Link>
        ))}
      </ul>
    </div>
  );
}

export default SearchComp;
