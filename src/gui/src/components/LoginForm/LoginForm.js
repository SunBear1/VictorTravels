import {GiBoarTusks} from 'react-icons/gi';
import {Link} from 'react-router-dom';
import {useContext, useState} from 'react';
import axios from 'axios';
import {UserContext} from '../../UserProvider';
import parseResponse from '../../useResponse';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const {login} = useContext(UserContext);

  const [message, setMessage] = useState(null);
  const [isGood, setIsGood] = useState(false);

  const handleSubmit = async event => {
    event.preventDefault();
    try {
      const response = await axios.post(
          'http://localhost:18000/api/v1/users/login',
          {
            email,
            password,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
      );
      const token = response.headers.authorization;
      login(token);
      const [mess, isGood] = parseResponse('login_POST', response);
      setMessage(mess);
      setIsGood(isGood);
      window.location.reload();
    } catch (error) {
      console.error(error);
      const [mess, isGood] = parseResponse('login_POST', error.response);
      setMessage(mess);
      setIsGood(isGood);
    }
  };
  return (
      <div className="flex min-h-full flex-col justify-center px-6 lg:px-8 h-[calc(100vh-74px)]">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <GiBoarTusks className="mx-auto" color="#e2e8f0" size={50}/>
          <h2 className="mt-5 text-center text-2xl font-bold leading-9 tracking-tight text-slate-300">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label
                  htmlFor="email"
                  className="block text-sm font-medium leading-6 text-slate-300"
              >
                Email address
              </label>
              <div className="mt-2">
                <input
                    id="email"
                    name="email"
                    type="email"
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    required
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label
                    htmlFor="password"
                    className="block text-sm font-medium leading-6 text-slate-300"
                >
                  Password
                </label>
              </div>
              <div className="mt-2">
                <input
                    id="password"
                    name="password"
                    type="password"
                    required
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
              </div>
            </div>

            <div>
              <button
                  type="submit"
                  className="flex w-full justify-center rounded-md bg-cyan-400 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-cyan-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Sign in
              </button>
            </div>
          </form>
          {!isGood &&
              <div
                  className="flex mt-10 p-4 mb-4 text-sm text-red-800 border border-red-300 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400 dark:border-red-800"
                  role="alert"
              >
                <svg
                    aria-hidden="true"
                    className="flex-shrink-0 inline w-5 h-5 mr-3"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clipRule="evenodd"
                  />
                </svg>
                <span className="sr-only">Info</span>
                <div>
                  <span className="font-medium">Error!</span> {message}
                </div>
              </div>}
          {isGood &&
              <div
                  className="flex mt-5 p-4 mb-4 text-sm text-green-800 border border-green-300 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400 dark:border-green-800"
                  role="alert"
              >
                <svg
                    aria-hidden="true"
                    className="flex-shrink-0 inline w-5 h-5 mr-3"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                      fillRule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                      clipRule="evenodd"
                  />
                </svg>
                <span className="sr-only">Info</span>
                <div>
                  <span className="font-medium">Success!</span> {message}!
                </div>
              </div>}

          <p className="mt-10 text-center text-sm text-gray-500">
            Not a member?
            <Link
                to="/register"
                className="font-semibold leading-6 text-cyan-400 hover:text-cyan-500 ml-2"
            >
              Register now
            </Link>
          </p>
        </div>
      </div>
  );
}

export default LoginForm;
