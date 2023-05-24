import React from 'react';
import Card from '../Card/Card';

function TripList({trips}) {
  return (
      <div>
        {trips.map(trip => <Card key={trip} trip={trip}/>)}
      </div>
  );
}

export default TripList;
