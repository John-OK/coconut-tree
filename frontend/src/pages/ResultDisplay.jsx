import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ResultDisplay = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const result = location.state?.result;
  
    if (!result) {
      navigate('/');
      return null;
    }
  
    return (
      <div>
        <h2>Submission Result</h2>
        <p>
          {result.count > 1 
            ? `"${result.input}" has been submitted ${result.count} times.`
            : `You are the first user to submit "${result.input}".`}
        </p>
        <button onClick={() => navigate('/')}>Submit Another Answer</button>
      </div>
    );
  };

  export default ResultDisplay