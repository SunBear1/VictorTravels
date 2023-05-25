const WebSocket = require('ws');

const socket = new WebSocket('ws://127.0.0.1:18000/ws/events/preferences');

socket.addEventListener('message', (event) => {
    const eventData = JSON.parse(event.data);
    // Update the UI with the received event data
    console.log('Received event:', eventData);
});
