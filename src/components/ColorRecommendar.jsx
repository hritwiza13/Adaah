import React, { useState } from 'react';
import axios from 'axios';
import './ColorRecommendar.css';

const ColorRecommender = () => {
  const [file, setFile] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    if (!file) {
      setError('Please select an image first');
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await axios.post(
        'http://localhost:5000/color-recommendation',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      setRecommendation(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="color-recommender">
      <h2>Outfit Color Analyzer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Outfit'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {recommendation && (
        <div className="results">
          <h3>Analysis Results:</h3>
          <div className="color-box" 
               style={{ backgroundColor: `rgb(${recommendation.dominant_rgb.join(',')})` }}>
          </div>
          <p>Dominant Color: {recommendation.color_name}</p>
          <p>Recommendation: {recommendation.suggestion}</p>
        </div>
      )}
    </div>
  );
};

export default ColorRecommender;