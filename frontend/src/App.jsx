import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css'
import Home from './pages/Home'
import ResultDisplay from './pages/ResultDisplay'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      const sessionToken = getCookie('session_token');
      if (sessionToken) {
        try {
          const response = await axios.get('/api/check-session/', {
            headers: {
              'X-Session-Token': sessionToken
            }
          });
          setIsAuthenticated(true);
          setUser(response.data.user);
        } catch (error) {
          console.error('Session validation failed:', error);
        }
      }
      setLoading(false);
    };

    checkSession();
  }, []);

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        {/* Add a navbar component here */}
        <Routes>
          <Route path="/" element={<Home isAuthenticated={isAuthenticated} user={user} />} />
          <Route path="/resultDisplay" element={<ResultDisplay />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;