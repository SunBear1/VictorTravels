import './App.css';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import LocationEnum from './LocationEnum';
import CounterComp from './CounterComp';
import DateRangePicker from './DateRangePicker';
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
  const [child1Counter, setChild1Counter] = useState(0);
  const [child2Counter, setChild2Counter] = useState(0);
  const [child3Counter, setChild3Counter] = useState(0);

  const handleLocationChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      setSelectedCountries([...selectedCountries, value]);
    } else {
      setSelectedCountries(selectedCountries.filter((color) => color !== value));
    }
  };

  const handleParentInputChange = (value, parentId) => {
    console.log("asdasd + " + value);
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
    navigate(`/trips?adult=${adultCounter}&child1=${child1Counter}&child2=${child2Counter}&child3=${child3Counter}&date-start=${formattedStartDate}&date-end=${formattedEndDate}&locations=${encodedList}`);
  }


  const handleSubmit1 = async (event) => {
    event.preventDefault();

    }

  return (
    <div className="Search">

      <div> 
      <h1>Date Range for Trip</h1>
      <DateRangePicker getValue={handleDateInputChange}/>
      </div>
      <div id='Osoby'>
        <div><CounterComp getValue={handleParentInputChange} parentId={1} text="Dorośli"/></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={2} text="Dzieci 1"/></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={3} text="Dzieci 2"/></div>
        <div><CounterComp getValue={handleParentInputChange} parentId={4} text="Dzieci 3"/></div>
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
          <div className='selectedLocationsList'><li key={option}>{option}</li><br/></div>
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
      <br/>
      <button onClick={handleSubmit1}>Szukaj</button>

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
}

export default SearchComp;
