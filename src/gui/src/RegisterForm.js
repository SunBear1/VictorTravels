import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./RegisterForm.css"
import axios from 'axios';
import parseResponse from './useResponse';

const RegisterForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);
  const [isGood, setIsGood] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:18000/api/v1/users/register', {
        email: email,
        password: password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response);
      const [mess, isGood] = parseResponse("register_POST",response);
      setMessage(mess);
      setIsGood(isGood);
    } catch (error) {
      console.error(error)
      const [mess, isGood] = parseResponse("register_POST", error.response);
      setMessage(mess);
      setIsGood(isGood);
    }
  };

  return (
    <div className="register-form">
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="email" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Register</button>
      </form>
      {isGood && <p className="good">{message}</p>}
      {!isGood && <p className="error">{message}</p>}
      <p>Already have an account? <Link to="/login">Login</Link></p>
    </div>
  );
};

export default RegisterForm;
