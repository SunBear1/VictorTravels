import {useParams} from 'react-router-dom';
import axios from 'axios';
import {useContext, useEffect, useState} from 'react';
import useAuth from '../useAuth';
import {UserContext} from '../UserProvider';
import ReservationInfo from '../components/ReservationInfo/ReservationInfo';

function TripDetails() {
  const {id} = useParams();
  const [trip, setTrip] = useState(null);
  const isLoggedIn = useAuth();

  useEffect(
      () => {
        axios
            .get(`http://localhost:18000/api/v1/trips/trip/${id}`)
            .then(response => {
              setTrip(response.data);
            })
            .catch(error => {
              console.error(error);
            });
      },
      [id]
  );

  const {itemInCart, addToCart} = useContext(UserContext);

  const isReserved = itemInCart(id);

  const [selectedRoom, setSelectedRoom] = useState('');

  const [selectedDiet, setSelectedDiet] = useState('');
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

  useEffect(
      () => {
        const sum = adultNumber + kidsTo3yo + kidsTo10yo + kidsTo18yo;
        if (sum === 0) {
          setSelectedRoom(null);
        } else if (sum === 1) {
          const roomType = 'studio';
          if (trip.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
        } else if (sum === 2) {
          const roomType = 'small';
          if (trip.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
        } else if (sum === 3) {
          const roomType = 'medium';
          if (trip.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
        } else if (sum === 4) {
          const roomType = 'large';
          if (trip.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
        } else {
          const roomType = 'apartment';
          if (trip.hotel.rooms[roomType].available > 0)
            setSelectedRoom(roomType);
        }
      },
      [adultNumber, kidsTo10yo, kidsTo3yo, kidsTo18yo]
  );

  useEffect(
      () => {
        const fetchPrice = async () => {
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
  const handleReservation = () => {
    console.log('abba');
  };

  // const handleResravation = async event => {
  //   event.preventDefault ();
  //   const sum = adultNumber + kidsTo3yo + kidsTo10yo + kidsTo18yo;
  //   const token = Cookies.get ('token');
  //   const data = {
  //     hotel_id: trip.hotel.hotelId,
  //     room_type: selectedRoom,
  //     connection_id_to: ownTransportTo ? null : transportToId,
  //     connection_id_from: ownTransportFrom ? null : transportToId,
  //     head_count: sum,
  //     price: finalPrice,
  //   };
  //   const config = {
  //     headers: {Authorization: token},
  //   };

  //   try {
  //     const response = await axios.post (
  //       'http://localhost:18000/api/v1/reservations/' + trip.id,
  //       data,
  //       config
  //     );
  //     console.log (response.data);
  //     addToCart (trip.id);
  //   } catch (error) {
  //     console.error (error);
  //   }
  // };

  const handleTransportFromBooking = (cost, id) => {
    setTransportFromCost(cost);
    setTransportFromId(id);
  };

  const handleTransportToBooking = (cost, id) => {
    setTransportToCost(cost);
    setTransportToId(id);
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
                  <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700"/>
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
                  <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700"/>
                  <h3 className="text-xl font-bold dark:text-white">Diets:</h3>
                  <ul className="max-w-md space-y-1 text-gray-500 list-disc list-inside dark:text-gray-400">
                    {Object.keys(trip.hotel.diet).map(diet => (
                        <li key={diet} className="ml-5">
                          {diet} - {trip.hotel.diet[diet]}zł
                        </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="w-96 m-auto mt-5">
                <hr className="h-px my-2 bg-gray-200 border-0 dark:bg-gray-700"/>
                {!isLoggedIn &&
                    <div className="text-xl font-regular dark:text-white">
                      LOG IN TO BOOK
                    </div>}
              </div>
              <div className="flex justify-center">
                {isLoggedIn &&
                    <ReservationInfo
                        setAdultNumber={setAdultNumber}
                        setKidsTo3yo={setKidsTo3yo}
                        setKidsTo10yo={setKidsTo10yo}
                        setKidsTo18yo={setKidsTo18yo}
                        ownTransportFrom={ownTransportFrom}
                        ownTransportTo={ownTransportTo}
                        setOwnTransportFrom={setOwnTransportFrom}
                        trip={trip}
                        handleTransportFromBooking={handleTransportFromBooking}
                        handleTransportToBooking={handleTransportToBooking}
                        selectedDiet={selectedDiet}
                        selectedRoom={selectedRoom}
                        setSelectedDiet={setSelectedDiet}
                        isReserved={isReserved}
                        finalPrice={finalPrice}
                        handleResravation={handleResravation}
                    />}
              </div>
            </div>}
      </div>
  );
}

export default TripDetails;
