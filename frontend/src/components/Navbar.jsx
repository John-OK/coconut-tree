import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isAuthenticated, onSignIn, onSignUp, onLogout }) => {
  return (
    <nav className="navbar" role="navigation" aria-label="main navigation">
      <div className="navbar-brand">
        <Link to="/" className="navbar-item">
          <strong>Trump Trump!</strong>
        </Link>
      </div>

      <div className="navbar-end">
        <div className="navbar-item">
          <div className="buttons">
            {isAuthenticated ? (
              <button onClick={onLogout} className="button is-light">
                Log out
              </button>
            ) : (
              <>
                <button onClick={onSignUp} className="button is-primary">
                  <strong>Sign up</strong>
                </button>
                <button onClick={onSignIn} className="button is-light">
                  Sign in
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
