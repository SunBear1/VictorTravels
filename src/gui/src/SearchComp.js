import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import LocationEnum from './LocationEnum';
import CounterComp from './CounterComp';
import DateRangePicker from './DateRangePicker';
import "./SearchComp.css"

function SearchComp() {

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
  }

  return (
    <div className="Search">

      <div> 
      <h1>Date Range Picker Examples</h1>
      <DateRangePicker />
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
      <button onClick={handleSubmit}>Szukaj</button>
    </div>
  );
}

export default SearchComp;
