import { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from './UserProvider';
import './LoginForm.css';
import parseResponse from './useResponse';

const LoginForm = () => {
  
  const navigate = useNavigate();
  const [loginId, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(UserContext);
  
  const [message, setMessage] = useState(null);
  const [isGood, setIsGood] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:18000/api/v1/users/login', {
        email: loginId,
        password: password
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      const token = response.headers.authorization;
      console.log(token);
      login(token);
      const [mess, isGood] = parseResponse("login_POST",response);
      setMessage(mess);
      setIsGood(isGood);
      window.location.reload();
    } catch (error) {
      console.error(error)
      const [mess, isGood] = parseResponse("login_POST", error.response);
      setMessage(mess);
      setIsGood(isGood);
    }
  };

  return (
    <div className="login-form-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="login-id">Login ID (EMAIL)</label>
          <input type="text" id="login-id" name="loginId" value={loginId} onChange={(e) => setLoginId(e.target.value)} required />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        <button type="submit">Sign In</button>
        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </form>
      
      {isGood && <p className="good">{message}</p>}
      {!isGood && <p className="error">{message}</p>}
    </div>
  );
}

export default LoginForm;
