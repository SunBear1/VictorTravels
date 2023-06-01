import {useState} from 'react';
import SearchBar from '../components/SearchBar/SearchBar';
import TripList from '../components/TripList/TripList';

function Search() {
    const [trips, setTrips] = useState(null);

    return (
        <div>
            <div className="flex justify-center mt-10">
                <SearchBar setTrips={setTrips}/>
            </div>
            {trips
                ? <div className="flex justify-center mt-10">
                    <TripList trips={trips}/>
                </div>
                : null}
        </div>
    );
}

export default Search;
