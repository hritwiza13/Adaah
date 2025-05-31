import React from 'react';
import './displayfit.css';

import { useLocation } from 'react-router'; 
const DisplayFit = () => {
  const { state } = useLocation(); 

  return (
    <div className="result-container">
      <h2>Your Perfect Outfit</h2>
      {state?.data ? (
        <div>
          <img 
            src={`http://localhost:5000/${state.data.image_path}`} 
            alt="Uploaded outfit"
            style={{ maxWidth: '500px', height: 'auto' }}
          />
          <p><strong>Occasion:</strong> {state.data.occasion}</p>
          <p><strong>Weather:</strong> {state.data.weather}</p>
        </div>
      ) : (
        <p>No outfit data found.</p>
      )}
    </div>
  );
};

export default DisplayFit;
