import axios from "axios";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

function Home() {
  const [userInput, setUserInput] = useState("");
  const [charCount, setCharCount] = useState(0);
  const navigate = useNavigate();
  const maxLength = 25;

  useEffect(() => {
    setCharCount(userInput.length);
  }, [userInput]);

  const handleSubmit = async () => {
    if (userInput.trim() === "" || userInput.length > maxLength) {
      alert(
        `Input must not be empty and should be ${maxLength} characters or less.`
      );
      return;
    }

    try {
      const response = await axios.post("/user_answer", {
        answer: userInput.toLowerCase(),
      });
      navigate("/resultDisplay", { state: { result: response.data } });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleInputChange = (event) => {
    const input = event.target.value;
    if (input.length <= maxLength) {
      setUserInput(input);
    }
  };

  const getCharCountColor = () => {
    if (charCount > maxLength) return "red";
    if (charCount > maxLength - 5) return "orange";
    return "white";
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
          // maxLength={maxLength}
        />
        <div className="char-count" style={{ color: getCharCountColor() }}>
          {charCount}/{maxLength}
        </div>
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
