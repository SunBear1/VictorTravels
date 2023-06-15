import {Route, Routes} from 'react-router-dom';
import PrivateRoute from './routes/PrivateRoute';
import Buy from './pages/Buy';
import LoginRoute from './routes/LoginRoute';
import Navbar from './components/Navbar/Navbar';
import LoginForm from './components/LoginForm/LoginForm';
import RegisterForm from './components/RegisterForm/RegisterForm';
import Search from './pages/Search';
import TripDetails from './pages/TripDetails';
import Cart from './pages/Cart';
import History from './pages/History';
import WebSocketPreference from './components/WebSocket/WebSocketPreference';

const App = () => {
  return (
      <div>
        <Navbar/>
        <WebSocketPreference/>
        <Routes>
          <Route path="/history" element={<History/>}/>

          <Route path="/"/>
          <Route path="/search" element={<Search/>}/>

          <Route exact path="/login" element={<LoginRoute/>}>
            <Route path="/login" element={<LoginForm/>}/>
          </Route>

          <Route path="/search/trip/:id" element={<TripDetails/>}/>
          <Route path="/register" element={<RegisterForm/>}/>

          <Route exact path="/cart" element={<PrivateRoute/>}>
            <Route exact path="/cart" element={<Cart/>}/>
          </Route>

          <Route exact path="/:id/buy" element={<PrivateRoute/>}>
            <Route exact path="/:id/buy" element={<Buy/>}/>
          </Route>
        </Routes>
      </div>
  );
};

export default App;
