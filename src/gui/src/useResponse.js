import { useState, useEffect } from 'react';
import axios from 'axios';

const parseResponse = (type, response) => {

    var message = "";
    var isGood = false;
    if (response.status === 200) 
    {

        if(type === "login_POST")message = 'User successfully logged in';
        if(type === "register_POST")message = 'User successfully registered';
        if(type === "payments_POST")message = 'Payment performed successfully';
        if(type === "purchases_POST")message = 'Purchase was already performed';
        if(type === "reservations_POST")message = 'Successful Response';
        if(type === "trip_GET")message = 'Trip data successfully listed';
        if(type === "trips_GET")message = 'Trips fetched successfully';
        isGood = true;

    } else if (response.status === 201) 
    {
        if(type === "register_POST")message = 'User successfully registered';
        if(type === "purchases_POST")message = 'Purchase successfully created';
        if(type === "reservations_POST")message = 'Reservation successfully created';
        isGood = true;

    } else if (response.status === 400) 
    {
        if(type === "payments_POST")message = 'Reservation with provided ID has already been paid for';
        if(type === "reservations_POST")message = 'Trip with provided ID does not have enough places left';
        if(type === "trips_GET")message = 'Invalid tour researcher query parameters';

    } else if (response.status === 401) 
    {
        if(type === "login_POST")message = 'Users provided credentials does not match';

    } else if (response.status === 402) 
    {
        if(type === "payments_POST")message = 'Payment for reservation have failed';

    } else if (response.status === 403) 
    {
        if(type === "payments_POST")message = 'User does not have permission to use this service';
        if(type === "purchases_POST")message = 'User does not have permission to use this service';
        if(type === "reservations_POST")message = 'User does not have permission to use this service';
        if(type === "trip_GET")message = 'User does not have permission to use this service';
        if(type === "trips_GET")message = 'User does not have permission to use this service';

    } else if (response.status === 404) 
    {
        if(type === "payments_POST")message = 'Reservation with provided ID does not exist';
        if(type === "purchases_POST")message = 'Reservation with provided ID does not exist';
        if(type === "reservations_POST")message = 'Trip with provided ID does not exist';
        if(type === "trip_GET")message = 'Trip with provided ID does not exist';

    } else if (response.status === 409) 
    {
        if(type === "register_POST")message = 'User with provided login already exists';

    } else if (response.status === 410) 
    {
        if(type === "payments_POST")message = 'Reservation with ID has expired';

    } else if (response.status === 422) 
    {
        if(type === "login_POST")message = 'Validation Error';
        if(type === "register_POST")message = 'Users data is invalid';
        if(type === "payments_POST")message = 'Validation Error';
        if(type === "purchases_POST")message = 'Unknown error occurred';
        if(type === "reservations_POST")message = 'Unknown error occurred';
        if(type === "trip_GET")message = 'Unknown error occurred';
        if(type === "trips_GET")message = 'Unknown error occurred';

    } else {
        message = 'An error occurred';
    }

    return [message, isGood];
};

export default parseResponse;
