import React from 'react';
import { FaHeart, FaLinkedin } from 'react-icons/fa';

function Footer() {
  return (
    <footer className="footer">
      <p>
        Made with <FaHeart className="heart" /> by{' '}
        <a
          href="https://www.linkedin.com/in/-satheesh-k/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Satheesh K <FaLinkedin />
        </a>
      </p>
    </footer>
  );
}

export default Footer;