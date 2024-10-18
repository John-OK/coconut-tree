import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../App.css";

const ResultDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) {
    navigate("/");
    return null;
  }

  return (
    <div className="home-container">
      <div className="result-header">
        <h1 className="result-input outfit-font">{result.input}</h1>
        <h2 className="trumps-text outfit-font">TRUMPS</h2>
        <h3 className="trump-text outfit-font">Trump</h3>
      </div>

      <div className="result-stats section">
        <p>
          "<span className="result-input-stats">{result.input}</span>"{" "}
          {result.count > 1
            ? `has been submitted ${result.count} times.`
            : `You are the first user to submit this.`}
        </p>
      </div>

      <div className="rankings section">
        <h2 className="others-input">Here's what others have said</h2>
        <h3 className="top-submissions">
          Top {result.top_inputs.length} Submissions
        </h3>
        <hr className="submissions-separator" />
        <ol>
          {result.top_inputs.map((item, index) => (
            <li key={index}>
              "<span className="result-input-stats">{item.input_text}</span>"{" "}
              (Submitted {item.count} times)
            </li>
          ))}
        </ol>
      </div>

      <button className="submit-button" onClick={() => navigate("/")}>
        Submit Another Answer
      </button>
    </div>
  );
};

export default ResultDisplay;
