import {useEffect, useState} from 'react';
import DatePicker from 'react-tailwindcss-datepicker';
import NumberInput from '../NumberInput/NumberInput';
import Select from 'react-select';
import axios from 'axios';

function SearchBar({setTrips}) {
  const [date, setDate] = useState([null, null]);
  const [departureLocations, setDepartureLocations] = useState([]);
  const [arrivalLocations, setArrivalLocations] = useState([]);
  const [selectedArrivalLocations, setSelectedArrivalLocations] = useState([]);
  const [selectedDepartureLocations, setSelectedDepartureLocations] = useState(
      []
  );
  const [adultNumber, setAdultNumber] = useState(1);
  const [kidsTo3yo, setKidsTo3yo] = useState(0);
  const [kidsTo10yo, setKidsTo10yo] = useState(0);
  const [kidsTo18yo, setKidsTo18yo] = useState(0);
  const [selectedTransport, setSelectedTransport] = useState([]);
  const [selectedDiet, setSelectedDiet] = useState([]);
  const [selectedMaxPrice, setSelectedMaxPrice] = useState(1200);
  const [maxPriceError, setMaxPriceError] = useState(false);

  const handleDateChange = selectedDate => {
    setDate(selectedDate);
  };

  const getLocations = async () => {
    const res = await axios.get(
        'http://localhost:18000/api/v1/trips/configurations'
    );
    setArrivalLocations(
        res.data.arrivalLocations.map(({country, region}) => ({
          value: country.toLowerCase(),
          label: country,
        }))
    );

    setDepartureLocations(
        res.data.departureLocations.map(city => ({
          value: city,
          label: city,
        }))
    );
  };

  const setHandleDepartureLocations = e => {
    setSelectedDepartureLocations(
        Array.isArray(e) ? e.map(location => location.label) : []
    );
  };

  const setHandleArrivalLocations = e => {
    setSelectedArrivalLocations(
        Array.isArray(e) ? e.map(location => location.label) : []
    );
  };

  const setHandleTransport = e => {
    setSelectedTransport(
        Array.isArray(e) ? e.map(transport => transport.label) : []
    );
  };

  const setHandleDiet = e => {
    setSelectedDiet(
        Array.isArray(e) ? e.map(diet => diet.value) : []
    );
  };

  const setMaxPrice = e => {
    if (e.target.value < 1) {
      console.log("DUPSKO")
      setMaxPriceError(true);
    } else {
      setSelectedMaxPrice(e.target.value);
      setMaxPriceError(false);
    }
  }

  function filterByUniqueTripId(arr) {
    const uniqueTripIds = {};

    const filteredArray = arr.filter(item => {
      if (!uniqueTripIds[item.tripID]) {
        uniqueTripIds[item.tripID] = true;
        return true;
      }
      return false;
    });

    return filteredArray;
  }

  function convertArrayToString(array) {
    if (array.length === 0) {
      return null;
    }
    return array.join(', ');
  }

  const handleSubmit = async e => {
    e.preventDefault();
    console.log(convertArrayToString(selectedArrivalLocations));
    await axios
        .get(
            'http://localhost:18000/api/v1/trips',
            {
              params: {
                adults: adultNumber,
                kids_to_3yo: kidsTo3yo,
                kids_to_10yo: kidsTo10yo,
                kids_to_18yo: kidsTo18yo,
                date_from: date.startDate,
                date_to: date.endDate,
                arrival_region: convertArrayToString(selectedArrivalLocations),
                departure_region: convertArrayToString(selectedDepartureLocations),
                transport: convertArrayToString(selectedTransport),
                diet: convertArrayToString(selectedDiet),
                max_price: selectedMaxPrice,
              },
            },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
        )
        .then(res => {
          setTrips(filterByUniqueTripId(res.data));
        })
        .catch(err => {
          console.log(err);
        });
  };

  const transportType = [
    {value: 'own', label: 'own'},
    {value: 'train', label: 'train'},
    {value: 'plane', label: 'plane'},
  ];

  const dietType = [
    {value: 'AllInclusive', label: 'All inclusive'},
    {value: 'Breakfast', label: 'Breakfast'},
    {value: 'TwoMeals', label: 'Two meals'},
    {value: 'None', label: 'No diet'},
  ];

  useEffect(() => {
    getLocations();
  }, []);

  return (
      <div>
        <p className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          Date range trip:
        </p>
        <div className="w-90 border border-slate-700 rounded">
          <DatePicker
              minDate={new Date()}
              separator={'to'}
              value={date}
              onChange={handleDateChange}
          />
        </div>
        <div className="mt-6 flex gap-2.5">
          <NumberInput label="Adults" defaultValue={1} val={setAdultNumber}/>
          <NumberInput label="Kids to 3 y/o" val={setKidsTo3yo}/>
          <NumberInput label="Kids to 10 y/o" val={setKidsTo10yo}/>
          <NumberInput label="Kids to 18 y/o" val={setKidsTo18yo}/>
        </div>
        <div className="mt-10">
          <div className="mx-auto container">
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Select arrival locations
            </label>
            <div className="flex flex-wrap items-center lg:justify-between justify-center">
              <div className="px-2">
                <Select
                    options={arrivalLocations}
                    onChange={setHandleArrivalLocations}
                    isMulti
                />
              </div>
            </div>
          </div>
          <div className="mt-2">
            <div className="mx-auto container">
              <label className="block text-sm font-medium text-gray-900 dark:text-white">
                Select departure locations
              </label>
              <div className="flex flex-wrap items-center lg:justify-between justify-center">
                <div className="px-2">
                  <Select
                      options={departureLocations}
                      onChange={setHandleDepartureLocations}
                      isMulti
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-2">
          <div className="mx-auto container">
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Select transport type
            </label>
            <div className="flex flex-wrap items-center lg:justify-between justify-center">
              <div className="px-2">
                <Select
                    options={transportType}
                    defaultValue={{value: 'own', label: 'own'}}
                    onChange={setHandleTransport}
                    isMulti
                />
              </div>
            </div>
          </div>
        </div>
        <div className="mt-2">
          <div className="mx-auto container">
            <label className="block text-sm font-medium text-gray-900 dark:text-white">
              Select diet type
            </label>
            <div className="flex flex-wrap items-center lg:justify-between justify-center">
              <div className="px-2">
                <Select
                    options={dietType}
                    defaultValue={{value: 'AllInclusive', label: 'All inclusive'}}
                    onChange={setHandleDiet}
                    isMulti
                />
              </div>
            </div>
          </div>
        </div>
        <div className="mt-2">
          <label htmlFor="default-input" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Max
            trip offer price</label>
          <input type="number" id="default-input"
                 className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                 defaultValue={selectedMaxPrice}
                 min={1}
                 onChange={setMaxPrice}/>
        </div>
        {maxPriceError ?
            <div className="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
                 role="alert">
              <span className="font-medium">Price value error</span> Minimum price must be at least 1.
            </div> : null
        }
        <button
            onClick={handleSubmit}
            className="mt-5 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded"
        >
          Submit
        </button>
      </div>
  );
}

export default SearchBar;
