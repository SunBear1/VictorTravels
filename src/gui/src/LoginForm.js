import { useContext, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { UserContext } from './UserProvider';
import './LoginForm.css';

const LoginForm = () => {
  const [loginId, setLoginId] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(UserContext);
  const [error, setError] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/auth/login', { loginId, password });
      const token = response.data.token;
      login(token);
    } catch (error) {
      setError(true);
    }

  };

  return (
    <div className="login-form-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="login-id">Login ID</label>
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
      {error && <div>Error</div>}
    </div>
  );
}

export default LoginForm;
