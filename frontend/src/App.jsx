import { useState } from 'react'
import './App.css'
import axios from "axios"

function App() {
  const [userInput, setUserInput] = useState("");
  const [submitResult, setSubmitResult] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await axios.post('/user_answer', {
        answer: userInput
      });
      
      setSubmitResult(response.data);
      setUserInput(''); // Clear the input field
    } catch (error) {
      console.error('Error:', error);
      // Handle errors (e.g., show error message to user)
    }
  };

  if (submitResult) {
    return <ResultDisplay result={submitResult} />;
  }

  return (
    <>
      <h1>Who trumps Trump?</h1>
      <h1>What trumps Trump?</h1>
      
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
    </>
  )
}

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  return (
    <div>
      <h2>Submission Result</h2>
      <p>
        {result.count > 1 
          ? `"${result.input}" has been submitted ${result.count} times.`
          : `You are the first user to submit "${result.input}".`}
      </p>
      <button onClick={() => window.location.reload()}>Submit Another Answer</button>
    </div>
  );
};

export default App
