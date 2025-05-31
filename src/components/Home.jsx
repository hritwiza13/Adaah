import React, { useState } from 'react';
import './home.css';
import { useNavigate } from 'react-router';

export default function Home() {
  const nav = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  function navigation(e) {
    e.preventDefault();
    nav('/upload-photo');
  }
  function navigateToRandomFit(e) {
    e.preventDefault();
    nav('/recommended-fit');
  }

  return (
    <main className="homepage">
      {/* Hamburger menu */}
      <div className="menu-container">
        <div className="hamburger" onClick={() => setIsMenuOpen(!isMenuOpen)}>
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>

        {isMenuOpen && (
          <div className="dropdown-menu">
            <p onClick={navigation}>Upload Photo</p>
            <br />
            <p onClick={navigateToRandomFit}>Our Recommended Fits</p>
          </div>
        )}
      </div>

      {/* Main content */}
      <div className="content">
        <h1 className="title">Adaah</h1>
        <p className="subtitle">Created By. HAVN.</p>
        <button className="cta" onClick={navigation}>Get Started</button>
      </div>
    </main>
  );
}
