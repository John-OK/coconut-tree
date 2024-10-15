import axios from 'axios';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

function Home({ isAuthenticated, user }) {
  const [userInput, setUserInput] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated && user) {
      setCurrentUser(user);
    }
  }, [isAuthenticated, user]);

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission
    try {
      const response = await axios.post(
        '/users/api/submit-form/',
        {
          answer: userInput,
        },
        {
          withCredentials: true, // This ensures cookies are sent with the request
        }
      );

      navigate('/resultDisplay', { state: { result: response.data } });
    } catch (error) {
      console.error('Error:', error);
      // Handle errors (e.g., show error message to user)
    }
  };

  return (
    <div
      className="Home container is-flex is-flex-direction-column is-justify-content-center"
      style={{ height: '100%' }}
    >
      <div className="content has-text-centered">
        <h1 className="title is-1">Who trumps Trump?</h1>
        <h1 className="title is-1">What trumps Trump?</h1>

        {isAuthenticated && currentUser ? (
          <p className="subtitle">Welcome, {currentUser.email}!</p>
        ) : (
          <p className="subtitle">Please log in to save your submissions.</p>
        )}

        <form onSubmit={handleSubmit}>
          <div className="field">
            <div className="control">
              <input
                className="input is-large"
                id="answer"
                type="text"
                name="user_answer"
                placeholder="Enter your idea"
                value={userInput}
                onChange={(event) => setUserInput(event.target.value)}
              />
            </div>
          </div>

          <button type="submit" className="button is-primary is-large">
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}

export default Home;
