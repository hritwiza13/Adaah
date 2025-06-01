import React, { useState } from 'react';
import './App.css';
import { uploadImage } from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [category, setCategory] = useState('tops');
  const [gender, setGender] = useState('men');
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setError(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const result = await uploadImage(selectedFile, category, gender);
      setRecommendations(result);
    } catch (err) {
      setError(err.message || 'An error occurred while getting recommendations');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Fashion Recommender</h1>
      </header>
      <main className="App-main">
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="form-group">
            <label>Select Category</label>
            <select value={category} onChange={(e) => setCategory(e.target.value)}>
              <option value="tops">Tops</option>
              <option value="bottoms">Bottoms</option>
            </select>
          </div>

          <div className="form-group">
            <label>Select Gender</label>
            <div className="gender-options">
              <label>
                <input
                  type="radio"
                  value="men"
                  checked={gender === 'men'}
                  onChange={(e) => setGender(e.target.value)}
                />
                Men
              </label>
              <label>
                <input
                  type="radio"
                  value="women"
                  checked={gender === 'women'}
                  onChange={(e) => setGender(e.target.value)}
                />
                Women
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Upload Image</label>
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              className="file-input"
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Getting recommendations...' : 'Get Recommendations'}
          </button>
        </form>

        {error && <div className="error-message">{error}</div>}

        {loading && <div className="loading">Loading...</div>}

        {recommendations && (
          <div className="recommendations">
            <h2>Recommendations</h2>
            <div className="recommendations-grid">
              {recommendations.map((item, index) => (
                <div key={index} className="recommendation-item">
                  <img src={item.image_url} alt={`Recommendation ${index + 1}`} />
                  <p>{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
