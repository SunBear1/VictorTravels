import { Routes, Route } from 'react-router-dom';
import SearchComp from './SearchComp';
import MyNavigation from './MyNavigation';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import TripList from './TripList';

const App = () => {
  return (
    <div>
          <MyNavigation/>
          <Routes>
            <Route path='/'/>
            <Route path="search" element={<SearchComp/>} />
            <Route path="trips" element={<TripList/>}/>
            <Route path="login" element={<LoginForm/>}/>
            <Route path="register" element={<RegisterForm/>}/>
          </Routes>
    </div>
  );
}

export default App;
