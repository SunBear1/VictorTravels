import React, { useEffect, useState } from 'react';
import "./history.css"

const WebSocketGenerated = () => {
    const [socket, setSocket] = useState(null);
    const [stack, setStack] = useState([]);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:18000/ws/events/generated');

        ws.onopen = () => {
            console.log('WebSocket generator connection established.');
        };

        ws.onmessage = (event) => {
            const receivedData = JSON.parse(event.data);
            console.log(receivedData);
            setStack([...stack, receivedData]);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed.');
        };

        setSocket(ws);

        // Clean up the effect
        return () => {
            ws.close();
        };
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