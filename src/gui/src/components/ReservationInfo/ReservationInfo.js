import NumberInput from '../NumberInput/NumberInput';
import TransportBooking from '../TransportBooking/TransportBooking';

function ReservationInfo({
                           setAdultNumber,
                           setKidsTo10yo,
                           setKidsTo18yo,
                           setKidsTo3yo,
                           ownTransportFrom,
                           ownTransportTo,
                           trip,
                           setOwnTransportFrom,
                           setOwnTransportTo,
                           handleTransportFromBooking,
                           handleTransportToBooking,
                           selectedDiet,
                           setSelectedDiet,
                           selectedRoom,
                           isReserved,
                           finalPrice,
                           handleResravation,
                         }) {
  return (
      <div className="flex">
        {trip &&
            <div>
              <div className="flex-row">
                <h3 className="mt-1 text-xl font-bold dark:text-white">
                  Number of people:
                </h3>
                <div className="flex gap-2.5">
                  <NumberInput
                      label="Adults"
                      defaultValue={1}
                      val={setAdultNumber}
                  />
                  <NumberInput label="Kids to 3 y/o" val={setKidsTo3yo}/>
                  <NumberInput label="Kids to 10 y/o" val={setKidsTo10yo}/>
                  <NumberInput label="Kids to 18 y/o" val={setKidsTo18yo}/>
                </div>
                <h3 className="mt-10 text-xl font-bold dark:text-white">
                  Transport from:
                </h3>
                <div className="flex items-center">
                  <input
                      checked={ownTransportFrom}
                      onChange={e => setOwnTransportFrom(e.target.checked)}
                      id="checked-checkbox"
                      type="checkbox"
                      className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <label className="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">
                    Own
                  </label>
                </div>
                <TransportBooking
                    locations={trip.from}
                    disable={ownTransportFrom}
                    getCost={handleTransportFromBooking}
                />
                <h3 className="mt-10 text-xl font-bold dark:text-white">
                  Transport to:
                </h3>
                <div className="flex items-center">
                  <input
                      checked={ownTransportTo}
                      onChange={e => setOwnTransportTo(e.target.checked)}
                      id="checked-checkbox"
                      type="checkbox"
                      className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <label className="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">
                    Own
                  </label>
                </div>
                <TransportBooking
                    locations={trip.to}
                    disable={ownTransportTo}
                    getCost={handleTransportToBooking}
                />
              </div>
              <div className="flex-col mt-1 ml-10">
                <h3 className="mt-10 text-xl font-bold dark:text-white">Diet:</h3>
                <div>
                  <select
                      id="diet-select"
                      value={selectedDiet}
                      onChange={e => setSelectedDiet(e.target.value)}
                  >
                    <option value="">Select a diet</option>
                    {Object.keys(trip.hotel.diet).map(diet => (
                        <option key={diet} value={diet}>
                          {diet}
                        </option>
                    ))}
                  </select>
                </div>
                <div>
                  {selectedRoom &&
                      <p className="mt-10 text-xl font-bold dark:text-white">
                        Selected room: {selectedRoom}
                      </p>}
                </div>
                <h3 className="mt-10 text-xl font-bold dark:text-white">
                  Final price:
                </h3>
                {!isReserved &&
                    (finalPrice
                        ? <p className="text-xl font-bold dark:text-white">
                          {finalPrice} zł
                        </p>
                        : <p className="tracking-tight text-gray-500 md:text-lg dark:text-gray-400">
                          Loading
                        </p>)}
              </div>
                {!isReserved
                    ? selectedRoom &&
                    <button className="mt-5 mb-5 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded"
                            onClick={handleResravation}>
                        Rezerwuj teraz
                    </button>
                    : null}
            </div>}
      </div>
  );
}

export default ReservationInfo;
