import React, { useEffect, useState } from 'react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import "./modal.css"

const WebSocketPreference = () => {
    const [socket, setSocket] = useState(null);
    const [showModal1, setShowModal1] = useState(false);
    const [showModal2, setShowModal2] = useState(false);
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
        setShowModal1(true);
        setShowModal2(true);
        toast.success("Trip " + receivedData.tripID + " has been bought or reserved",{position:toast.POSITION.TOP_RIGHT})
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
  
  
    const handleCloseModal1 = () => {
      setShowModal1(false);
    };
    const handleCloseModal2 = () => {
      setShowModal2(false);
    };
  
    return (
      <div>
        <Modal show={showModal1} onHide={handleCloseModal1} className="modal">
          <Modal.Header closeButton className="modal-header">
            <Modal.Title className="modal-title"><b>Preferences direction trip</b></Modal.Title>
          </Modal.Header>
          <Modal.Body className="modal-body">
            <h1>Trip number {receivedMessage?.tripID}</h1>
            <p>To country: {receivedMessage?.country}</p>
            <p>To region: {receivedMessage?.region}</p>
          </Modal.Body>
          <Modal.Footer className="modal-footer">
            <Button variant="secondary" onClick={handleCloseModal1}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
        <Modal show={showModal2} onHide={handleCloseModal2} className="modal">
          <Modal.Header closeButton className="modal-header">
            <Modal.Title className="modal-title"><b>Preferences hotel, room, transport trip</b></Modal.Title>
          </Modal.Header>
          <Modal.Body className="modal-body">
            <h1>Trip number {receivedMessage?.tripID}</h1>
            <p>Hotel: {receivedMessage?.hotelName}</p>
            <p>Room: {receivedMessage?.roomType}</p>
            <p>Transport: {receivedMessage.transportType ? receivedMessage?.transportType : "Own"}</p>
          </Modal.Body>
          <Modal.Footer className="modal-footer">
            <Button variant="secondary" onClick={handleCloseModal2}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
        <ToastContainer/>
      </div>
    );
  };
  
  
export default WebSocketPreference;