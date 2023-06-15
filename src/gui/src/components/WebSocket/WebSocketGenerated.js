import React, { useEffect, useState } from 'react';
import "./history.css"
import axios from 'axios';

const WebSocketGenerated = () => {
    const [stack, setStack] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
          try {
            const response = await axios.get('http://localhost:18000/api/v1/events/generated');
            const data = response.data;
            setStack(data);
            console.log(stack.length);
          } catch (error) {
            console.error('Error fetching data:', error);
          }
        };
    
        // Fetch data initially
        fetchData();
    
        // Fetch data every 20 seconds
        const intervalId = setInterval(fetchData, 20000);
    
        // Clean up the interval on component unmount
        return () => clearInterval(intervalId);
      }, []);


    return (
        <div>
            {stack.map((item) => (
                <div className='history'>
                    <ul>Name: {item.name}</ul>
                    <ul>Type: {item.type}</ul>
                    <ul>Resource: {item.resource}</ul>
                    <ul>Operation: {item.operation}</ul>
                    <ul>Value: {item.value}</ul>
                </div>
            ))}
        </div>
    );
};


export default WebSocketGenerated;