// THIS IS A MOCK PROGRAM FOR SIMULATING GUI WEBSOCKET SERVER


const WebSocket = require('ws');
const wss = new WebSocket.Server({port: 18005});

wss.on('connection', (ws) => {
  ws.on('message', (message) => {
    console.log('Received message:', JSON.parse(message));
  });

  ws.on('close', () => {
    console.log('Connection closed');
  });
});

console.log('WebSocket server started on port 18005');
