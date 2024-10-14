import { useState } from 'react'
import '../App.css'
import axios from "axios"
import { useNavigate } from 'react-router-dom';

function Home({ isAuthenticated, user }) {
    const [userInput, setUserInput] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async () => {
      try {
        const response = await axios.post('users/api/submit-form/', {
          answer: userInput
        }, {
          withCredentials: true // This ensures cookies are sent with the request
        });
        
        navigate('/resultDisplay', { state: { result: response.data } });
      } catch (error) {
        console.error('Error:', error);
        // Handle errors (e.g., show error message to user)
      }
    };

    return (
      <div className="Home">
        <h1>Who trumps Trump?</h1>
        <h1>What trumps Trump?</h1>

        {isAuthenticated ? (
          <p>Welcome, {user.email}!</p>
        ) : (
          <p>Please log in to save your submissions.</p>
        )}

        <h1>
        <form >
          <input
            className='answer'
            id="answer"
            type="text"
            name="user_answer"
            value={userInput}
            onChange={(event) => setUserInput(event.target.value)}
            placeholder="Enter your idea"
          />
        </form>
        </h1>
        <button
          className="submit"
          type="submit" onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
    )
  }

  export default Home