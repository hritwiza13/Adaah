import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import './details.css';
import './ColorAnalysis.css';

const Details = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name } = useParams();
  const { colorAnalysis, weather, occasion } = location.state || {};

  const [userDetails, setUserDetails] = useState({ name: '', email: '', password: '', birthday: '' });
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    // Load user details from localStorage
    const storedName = localStorage.getItem('user_name') || '';
    const storedEmail = localStorage.getItem('user_email') || '';
    const storedPassword = localStorage.getItem('user_password') || '';
    const storedBirthday = localStorage.getItem('user_birthday') || '';

    setUserDetails({ 
      name: storedName, 
      email: storedEmail, 
      password: storedPassword, 
      birthday: storedBirthday 
    });
  }, []);

  const handleEditToggle = () => setEditing(!editing);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setUserDetails((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = () => {
    // Save updated details to localStorage
    localStorage.setItem('user_name', userDetails.name);
    localStorage.setItem('user_email', userDetails.email);
    localStorage.setItem('user_birthday', userDetails.birthday);
    localStorage.setItem('email', userDetails.email);
    setEditing(false);
  };

  const handleBack = () => {
    navigate('/upload-photo');
  };

  // Get outfit suggestions if color analysis is available
  const outfitSuggestions = colorAnalysis ? [
    {
      title: `${weather || 'All Weather'} - ${occasion || 'All Occasions'} - Analogous`,
      description: `Harmonious blend of ${colorAnalysis.colorName} with adjacent hues for ${occasion || 'any'} occasion`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: colorAnalysis.analogous1Name, hex: colorAnalysis.analogous1 },
        { name: colorAnalysis.analogous2Name, hex: colorAnalysis.analogous2 }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} ${occasion || 'all'} analogous outfit ${colorAnalysis.colorName} fashion style`
    },
    {
      title: `${weather || 'All Weather'} - ${occasion || 'All Occasions'} - Complementary`,
      description: `Bold mix of ${colorAnalysis.colorName} with its complement for ${occasion || 'any'} occasion`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: colorAnalysis.complementaryName, hex: colorAnalysis.complementary }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} ${occasion || 'all'} complementary outfit ${colorAnalysis.colorName} contrast fashion`
    },
    {
      title: `${weather || 'All Weather'} - ${occasion || 'All Occasions'} - Monochromatic`,
      description: `Sophisticated tones of ${colorAnalysis.colorName} for ${occasion || 'any'} occasion`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: `${colorAnalysis.colorName} light`, hex: colorAnalysis.monochromatic1 },
        { name: `${colorAnalysis.colorName} dark`, hex: colorAnalysis.monochromatic2 }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} ${occasion || 'all'} monochromatic outfit ${colorAnalysis.colorName} fashion style`
    }
  ] : [];

  return (
    <div className="details-container">
      <h2 className="details-title">👤 User Details</h2>
      <div className="user-info">
        {editing ? (
          <>
            <label>Name:</label>
            <input name="name" value={userDetails.name} onChange={handleChange} />
            <label>Email:</label>
            <input name="email" value={userDetails.email} onChange={handleChange} />
            <label>Birthday:</label>
            <input type="date" name="birthday" value={userDetails.birthday} onChange={handleChange} />
            <button onClick={handleSave}>💾 Save</button>
          </>
        ) : (
          <>
            <p><strong>Name:</strong> {userDetails.name}</p>
            <p><strong>Email:</strong> {userDetails.email}</p>
            <p><strong>Birthday:</strong> {userDetails.birthday}</p>
            <button onClick={handleEditToggle}>✏ Edit</button>
          </>
        )}
      </div>

      {colorAnalysis && (
        <div className="color-analysis-section">
          <h2 className="outfits-title">🎨 Color Analysis Results</h2>
          <div className="outfit-suggestions">
            {outfitSuggestions.map((suggestion, index) => (
              <div key={index} className="suggestion-card">
                <h3>{suggestion.title}</h3>
                <p>{suggestion.description}</p>
                <div className="color-palette">
                  {suggestion.colors.map((color, colorIndex) => (
                    <div key={colorIndex} className="color-swatch">
                      <div 
                        className="color-box" 
                        style={{ backgroundColor: color.hex }}
                      />
                      <span>{color.name}</span>
                    </div>
                  ))}
                </div>
                <a 
                  href={suggestion.pinterestLink} 
                  target="_blank" 
                  rel="noreferrer"
                  className="pinterest-link"
                >
                  View Inspiration
                </a>
              </div>
            ))}
          </div>
          <button onClick={handleBack} className="back-button">
            Back to Upload
          </button>
        </div>
      )}
    </div>
  );
};

export default Details;