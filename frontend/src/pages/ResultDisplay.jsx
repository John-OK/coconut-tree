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
            <h1>
                {result.input} trumps Trump!
            </h1>
            <p>
            {result.count > 1 
                ? `"${result.input}" has been submitted ${result.count} times.`
                : `You are the first user to submit "${result.input}".`}
            </p>
            <h2>Here's what others have said</h2>
            <h3>Top {result.top_inputs.length} Submissions</h3>
            <ol>
                {result.top_inputs.map((item, index) => (
                <li key={index}>
                    {item.input_text} (Submitted {item.count} times)
                </li>
                ))}
            </ol>
            <button onClick={() => navigate('/')}>Submit Another Answer</button>
        </div>
    );
  };

  export default ResultDisplay