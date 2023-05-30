import {useEffect, useState} from 'react';
import Cookies from 'js-cookie';

const useAuth = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = Cookies.get('token');

        if (token) {
            setIsLoggedIn(true);
        }
    }, []);

    return isLoggedIn;
};

export default useAuth;
