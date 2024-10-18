import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

function Home() {
  const [userInput, setUserInput] = useState("");
  const navigate = useNavigate();
  const maxLength = 25;

  const handleSubmit = async () => {
    if (userInput.trim() === "" || userInput.length > maxLength) {
      // Show an error message to the user
      alert(
        "Input must not be empty and should be ${maxLength} characters or less."
      );
      return;
    }

    try {
      const response = await axios.post("/user_answer", {
        answer: userInput.toLowerCase(), // Store lowercase in the database
      });

      navigate("/resultDisplay", { state: { result: response.data } });
    } catch (error) {
      console.error("Error:", error);
      alert("Sorry. There was an error. Try refreshing your browser.");
    }
  };

  const handleInputChange = (event) => {
    const input = event.target.value;
    if (input.length <= maxLength) {
      setUserInput(input);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <div className="home-container">
      <div className="input-container">
        <input
          className="custom-input outfit-font"
          type="text"
          value={userInput}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Enter your idea"
          maxLength={maxLength}
        />
      </div>
      <h2 className="trumps-text outfit-font">TRUMPS</h2>
      <h3 className="trump-text outfit-font">Trump</h3>
      <button className="submit-button outfit-font" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
}

export default Home;
