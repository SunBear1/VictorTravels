import React from 'react';
import {Link} from 'react-router-dom';

function Card({trip}) {
    return (
        <div
            className="flex flex-col rounded-lg bg-white dark:bg-neutral-700 shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07),0_10px_20px_-2px_rgba(0,0,0,0.04)] md:max-w-7xl md:flex-row mb-5">
            <img
                className="h-96 w-full rounded-t-lg object-cover md:h-auto md:w-48 md:rounded-none md:rounded-l-lg"
                src={trip.hotel.image}
                alt=""
            />
            <div className="flex flex-col justify-start p-6 bg-white dark:bg-slate-700 w-full">
                <h5 className="mb-2 text-xl font-medium text-neutral-800 dark:text-neutral-50">
                    {trip.localisation.country} - {trip.localisation.region}
                </h5>
                <p className="mb-4 text-base text-neutral-600 dark:text-neutral-200">
                    {trip.hotel.name}
                </p>
                <p className="mb-4 text-base text-neutral-600 dark:text-neutral-200">
                    {trip.hotel.description.map(info => <li key={info}>{info}</li>)}
                </p>
                <p className="text-xs text-neutral-500 dark:text-neutral-300">
                    Average price per perSson: {trip.price}
                </p>
                <Link
                    to={'trip/' + trip.id}
                    className="text-white mt-5 bg-gradient-to-r from-cyan-500 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
                >
                    check the offer
                </Link>
            </div>
        </div>
    );
}

export default Card;
