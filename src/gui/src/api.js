import axios from 'axios';
import Cookies from 'js-cookie';

const api = axios.create({
    baseURL: 'https://example.com/api',
});

api.interceptors.request.use(config => {
    const token = Cookies.get('token');

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

api.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        const originalRequest = error.config;
        const token = Cookies.get('token');

        if (error.response.status === 401 && !originalRequest._retry && token) {
            originalRequest._retry = true;

            return api.post('/auth/refresh_token', {token}).then(response => {
                const newToken = response.headers.authorization.split(' ')[1];
                Cookies.set('token', newToken, {expires: 7, sameSite: 'strict'});

                originalRequest.headers.Authorization = `Bearer ${newToken}`;

                return api(originalRequest);
            });
        }

        return Promise.reject(error);
  }
);

export default api;
