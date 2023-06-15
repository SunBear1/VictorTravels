import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import "./modal.css"

const WebSocketPreference = () => {
    const [socket, setSocket] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [receivedMessage, setReceivedMessage] = useState('');
  
    useEffect(() => {
      const ws = new WebSocket('ws://localhost:18000/ws/events/preferences');
  
      ws.onopen = () => {
        console.log('WebSocket connection established.');
      };
  
      ws.onmessage = (event) => {
        const receivedData = JSON.parse(event.data);
        console.log(receivedData);
        setReceivedMessage(receivedData);
        setShowModal(true);
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
  
  
    const handleCloseModal = () => {
      setShowModal(false);
    };
  
    return (
      <div>
        <Modal show={showModal} onHide={handleCloseModal} className="modal">
          <Modal.Header closeButton className="modal-header">
            <Modal.Title className="modal-title"><b>Trip has been bought or reserved</b></Modal.Title>
          </Modal.Header>
          <Modal.Body className="modal-body">
            <h1>Trip number {receivedMessage?.tripID}</h1>
            <p>To country: {receivedMessage?.country}</p>
            <p>To region: {receivedMessage?.region}</p>
            <p>Hotel: {receivedMessage?.hotelName}</p>
            <p>Room: {receivedMessage?.roomType}</p>
            <p>Transport: {receivedMessage.transportType ? receivedMessage?.transportType : "Own"}</p>
          </Modal.Body>
          <Modal.Footer className="modal-footer">
            <Button variant="secondary" onClick={handleCloseModal}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  };
  
  
export default WebSocketPreference;