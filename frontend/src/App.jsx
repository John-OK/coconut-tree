import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css'
import Home from './pages/Home'
import ResultDisplay from './pages/ResultDisplay'
import Navbar from './components/Navbar';
import SignInModal from './components/SignInModal';
import SignUpModal from './components/SignUpModal';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSignInModalOpen, setIsSignInModalOpen] = useState(false);
  const [isSignUpModalOpen, setIsSignUpModalOpen] = useState(false);

  useEffect(() => {
    const checkSession = async () => {
      const sessionToken = getCookie('session_token');
      if (sessionToken) {
        try {
          const response = await axios.get('users/api/check-session/', {
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

  const handleSignIn = async (email, password) => {
    try {
      const response = await axios.post('/users/api/login/', { email, password });
      setIsAuthenticated(true);
      setUser(response.data.user);
      setIsSignInModalOpen(false);
    } catch (error) {
      console.error('Sign in failed:', error);
      // Handle error (e.g., show error message)
    }
  };

  const handleSignUp = async (email, password) => {
    try {
      const response = await axios.post('/users/api/register/', { email, password });
      setIsAuthenticated(true);
      setUser(response.data.user);
      setIsSignUpModalOpen(false);
    } catch (error) {
      console.error('Sign up failed:', error);
      // Handle error (e.g., show error message)
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('/users/api/logout/');
      setIsAuthenticated(false);
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
      // Handle error (e.g., show error message)
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navbar 
          isAuthenticated={isAuthenticated}
          onSignIn={() => setIsSignInModalOpen(true)}
          onSignUp={() => setIsSignUpModalOpen(true)}
          onLogout={handleLogout}
        />
        <Routes>
          <Route path="/" element={<Home isAuthenticated={isAuthenticated} user={user} />} />
          <Route path="/resultDisplay" element={<ResultDisplay />} />
        </Routes>
        <SignInModal 
          isOpen={isSignInModalOpen}
          onClose={() => setIsSignInModalOpen(false)}
          onSignIn={handleSignIn}
        />
        <SignUpModal 
          isOpen={isSignUpModalOpen}
          onClose={() => setIsSignUpModalOpen(false)}
          onSignUp={handleSignUp}
        />
      </div>
    </Router>
  );
}

export default App;