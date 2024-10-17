import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

function Home() {
  const [userInput, setUserInput] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    if (userInput.trim() === "" || userInput.length > 25) {
      // Show an error message to the user
      alert("Input must not be empty and should be 25 characters or less.");
      return;
    }

    try {
      const response = await axios.post("/user_answer", {
        answer: userInput.toLowerCase(), // Store lowercase in the database
      });

      navigate("/resultDisplay", { state: { result: response.data } });
    } catch (error) {
      console.error("Error:", error);
      // Handle errors (e.g., show error message to user)
    }
  };

  const handleInputChange = (event) => {
    setUserInput(event.target.value); // Store as-is, display will be uppercase
  };

  return (
    <div className="home-container">
      <div className="input-container">
        <input
          className="custom-input outfit-font"
          type="text"
          value={userInput}
          onChange={handleInputChange}
          placeholder="Enter your idea"
          maxLength={25}
        />
      </div>
      <h2 className="trumps-text outfit-font">TRUMPS</h2>
      <h3 className="trump-text outfit-font">Trump</h3>
      <button className="submit-button outfit-font" onClick={handleSubmit}>
        Submit
      </button>

      {/* Test for client */}
      {/* <hr />
      <h1 className="py-0 my-0trumps-text outfit-font">KEEP</h1>
      <h1 className="py-0 my-0trumps-text outfit-font">CALM</h1>
      <h4 className="py-0 my-0trump-text is-size- outfit-font">AND</h4>
      <h1 className="py-0 my-0trumps-text outfit-font">CARRY</h1>
      <h1 className="py-0 my-0trumps-text outfit-font">ON</h1> */}
    </div>
  );
}

export default Home;
