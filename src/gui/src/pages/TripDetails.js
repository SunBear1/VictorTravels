import {Link, useParams} from 'react-router-dom';
import axios from 'axios';
import {useContext, useEffect, useState} from 'react';
import useAuth from '../useAuth';
import {UserContext} from '../UserProvider';
import ReservationInfo from '../components/ReservationInfo/ReservationInfo';
import Cookies from "js-cookie";

function TripDetails() {
  const { id } = useParams();
  const [trip, setTrip] = useState(null);
  const isLoggedIn = useAuth();

  useEffect(
    () => {
      axios
        .get(`http://localhost:18000/api/v1/trips/trip/${id}`)
        .then(response => {
          console.log(response.data);
          setTrip(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    []
  );

  const { itemInCart, addToCart } = useContext(UserContext);

  const isReserved = itemInCart(id);

  const [selectedRoom, setSelectedRoom] = useState('');

  const [selectedDiet, setSelectedDiet] = useState('All inclusive');
  const [adultNumber, setAdultNumber] = useState(1);
  const [kidsTo3yo, setKidsTo3yo] = useState(0);
  const [kidsTo10yo, setKidsTo10yo] = useState(0);
  const [kidsTo18yo, setKidsTo18yo] = useState(0);

  const [transportFromCost, setTransportFromCost] = useState(null);
  const [transportFromId, setTransportFromId] = useState(null);
  const [transportToCost, setTransportToCost] = useState(null);
  const [transportToId, setTransportToId] = useState(null);
  const [ownTransportFrom, setOwnTransportFrom] = useState(true);
  const [ownTransportTo, setOwnTransportTo] = useState(true);

  const [numberOfDays, setNumberOfDays] = useState(null);

  const [finalPrice, setFinalPrice] = useState(null);

  const [addedToCart, setAddedToCart] = useState(false);

  useEffect(
      () => {
        const sum = adultNumber + kidsTo3yo + kidsTo10yo + kidsTo18yo;
        if (sum === 0) {
          setSelectedRoom(null);
        } else if (sum === 1) {
          const roomType = 'studio';
          if (trip?.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
      } else if (sum === 2) {
        const roomType = 'small';
        if (trip?.hotel.rooms[roomType].available > 0)
          setSelectedRoom(roomType);
      } else if (sum === 3) {
        const roomType = 'medium';
        if (trip?.hotel.rooms[roomType].available > 0)
          setSelectedRoom(roomType);
      } else if (sum === 4) {
        const roomType = 'large';
        if (trip?.hotel.rooms[roomType].available > 0)
          setSelectedRoom(roomType);
      } else {
        const roomType = 'apartment';
        if (trip?.hotel.rooms[roomType].available > 0)
          setSelectedRoom(roomType);
      }
    },
    [adultNumber, kidsTo10yo, kidsTo3yo, kidsTo18yo]
  );

  useEffect(
    () => {
      const fetchPrice = async () => {
        console.log(selectedRoom);
        console.log(transportToCost);
        console.log(transportFromCost);
        try {
          const response = await axios.get(
            'http://localhost:18000/api/v1/trips/price',
            {
              params: {
                adults: adultNumber,
                kids_to_3yo: kidsTo3yo,
                kids_to_10yo: kidsTo10yo,
                kids_to_18yo: kidsTo18yo,
                number_of_days: numberOfDays,
                room_cost: trip.hotel.rooms[selectedRoom].cost,
                diet_cost: trip.hotel.diet[selectedDiet],
                transport_to_cost: ownTransportTo ? null : transportToCost,
                transport_from_cost: ownTransportFrom
                  ? null
                  : transportFromCost,
              },
            },
            {
              headers: {
                'Content-Type': 'application/json',
              },
            }
          );
          setFinalPrice(response.data);
          console.log(response.data);
        } catch (error) {
          console.error(error);
        }
      };
      fetchPrice();
    },
    [
      ownTransportFrom,
      ownTransportTo,
      transportFromCost,
      transportToCost,
      selectedDiet,
      selectedRoom,
    ]
  );

  const handleTransportFromBooking = (cost, id) => {
    setTransportFromCost(cost);
    setTransportFromId(id);
  };

  const handleTransportToBooking = (cost, id) => {
    setTransportToCost(cost);
    setTransportToId(id);
  };

  const handleResravation = async event => {
    event.preventDefault();
    const sum = adultNumber + kidsTo3yo + kidsTo10yo + kidsTo18yo;
    const token = Cookies.get('token');
    const data = {
      hotel_id: trip.hotel.hotelId,
      room_type: selectedRoom,
      connection_id_to: ownTransportTo ? "own" : transportToId,
      connection_id_from: ownTransportFrom ? "own" : transportToId,
      head_count: sum,
      price: finalPrice,
    };
    const config = {
      headers: { Authorization: token },
    };
    console.log(data);
    try {
      const response = await axios.post(
        'http://localhost:18000/api/v1/reservations/' + trip.id,
        data,
        config
      );
      console.log(response.data);
      addToCart(trip.id, response.data.reservation_id);
      setAddedToCart(true);
    } catch (error) {
      setAddedToCart(false);
      console.error(error);
    }
  };

  return (
    <div>
      {trip &&
        <div>
          <div className="flex justify-center mt-20">
            <div className="flex items-center mr-20">
              <img
                className="h-auto max-w-xl rounded-lg shadow-xl dark:shadow-gray-800"
                src={trip.hotel.image}
                alt="image description"
              />
            </div>
            <div className="flex flex-col">
              <h1 className="text-5xl font-extrabold dark:text-white">
                {trip.localisation.country}
              </h1>
              <h2 className="text-5xl font-extrabold dark:text-white">
                {trip.localisation.region}
              </h2>
              <div className="tracking-wide text-gray-500 md:text-lg dark:text-gray-400">
                {trip.hotel.name}
              </div>
              <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700" />
              <h3 className="text-xl font-bold dark:text-white">
                Hotel description:
              </h3>
              <ul className="max-w-md space-y-1 text-gray-500 list-disc list-inside dark:text-gray-400">
                {trip.hotel.description.map(value => (
                  <li className="ml-5" key={value}>
                    {value}
                  </li>
                ))}
              </ul>
              <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700" />
              <h3 className="text-xl font-bold dark:text-white">Diets:</h3>
              <ul className="max-w-md space-y-1 text-gray-500 list-disc list-inside dark:text-gray-400">
                {Object.keys(trip.hotel.diet).map(diet => (
                  <li key={diet} className="ml-5">
                    {diet}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="w-96 m-auto mt-5">
            <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700" />
            {!isLoggedIn &&
              <div className="text-xl font-regular dark:text-white">
                LOG IN TO BOOK
              </div>}
          </div>
          <div className="flex justify-center">
            {isLoggedIn &&
                <div>
                  <ReservationInfo
                      setAdultNumber={setAdultNumber}
                      setKidsTo3yo={setKidsTo3yo}
                      setKidsTo10yo={setKidsTo10yo}
                      setKidsTo18yo={setKidsTo18yo}
                      ownTransportFrom={ownTransportFrom}
                      ownTransportTo={ownTransportTo}
                      setOwnTransportFrom={setOwnTransportFrom}
                      setOwnTransportTo={setOwnTransportTo}
                      trip={trip}
                      handleTransportFromBooking={handleTransportFromBooking}
                      handleTransportToBooking={handleTransportToBooking}
                      selectedDiet={selectedDiet}
                      selectedRoom={selectedRoom}
                      setSelectedDiet={setSelectedDiet}
                      isReserved={isReserved}
                      finalPrice={finalPrice}
                      handleResravation={handleResravation}
                  />
                  {addedToCart ?
                      <div id="alert-border-3"
                           className=" mt-4 flex p-4 mb-4 text-green-800 border-t-4 border-green-300 bg-green-50 dark:text-green-400 dark:bg-gray-800 dark:border-green-800"
                           role="alert">
                        <svg className="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                             xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd"
                                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                                clip-rule="evenodd"></path>
                        </svg>
                        <div className="ml-3 text-sm font-medium">
                          Trip offer successfully added to cart. <Link to="/cart"
                                                                       className="font-semibold underline hover:no-underline">Buy
                          it now!</Link>
                        </div>
                      </div> : null
                  }
                </div>
            }
          </div>
        </div>}
    </div>
  );
}

export default TripDetails;
