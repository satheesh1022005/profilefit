import React from 'react';
import { FaGithub } from 'react-icons/fa';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <span className="logo">ProfileFit AI</span>
        </div>
        <div className="navbar-links">
          <a
            href="https://github.com/satheesh1022005"
            target="_blank"
            rel="noopener noreferrer"
            className="github-link"
          >
            <FaGithub /> View on GitHub
          </a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;