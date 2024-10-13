import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isAuthenticated, onSignIn, onSignUp, onLogout }) => {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">Let's trump Trump</Link>
      <div className="navbar-links">
        {isAuthenticated ? (
          <button onClick={onLogout} className="navbar-link">Log out</button>
        ) : (
          <>
            <button onClick={onSignIn} className="navbar-link">Sign in</button>
            <button onClick={onSignUp} className="navbar-link">Sign up</button>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;