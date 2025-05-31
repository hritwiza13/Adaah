import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ColorAnalysis.css';

const ColorAnalysis = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { colorAnalysis, weather, occasion } = location.state || {};

  // Debug logging
  console.log('Location State:', location.state);
  console.log('Color Analysis:', colorAnalysis);

  if (!colorAnalysis) {
    return (
      <div className="error-container">
        <div className="error-message">No color analysis data available</div>
        <button 
          className="back-button"
          onClick={() => navigate('/upload-photo')}
        >
          Go Back
        </button>
      </div>
    );
  }

  const handleBack = () => {
    navigate('/upload-photo');
  };

  const handleUserDetails = () => {
    navigate('/user-details');
  };

  // Get outfit suggestions
  const outfitSuggestions = [
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
  ];

  // Add occasion-specific suggestions
  if (occasion === 'casual') {
    outfitSuggestions.push({
      title: `${weather || 'All Weather'} - Casual Style`,
      description: `Relaxed look with ${colorAnalysis.colorName} accents for casual occasions`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: 'Neutral', hex: '#f5f5f5' },
        { name: 'Denim', hex: '#6f8faf' }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} casual street style outfit ${colorAnalysis.colorName} fashion`
    });
  } else if (occasion === 'formal') {
    outfitSuggestions.push({
      title: `${weather || 'All Weather'} - Formal Elegance`,
      description: `Elegant ensemble featuring ${colorAnalysis.colorName} for formal occasions`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: 'Black', hex: '#000000' },
        { name: 'White', hex: '#ffffff' }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} formal elegant outfit ${colorAnalysis.colorName} fashion`
    });
  } else if (occasion === 'party') {
    outfitSuggestions.push({
      title: `${weather || 'All Weather'} - Party Glam`,
      description: `Glamorous look with ${colorAnalysis.colorName} highlights for party occasions`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: 'Gold', hex: '#ffd700' },
        { name: 'Silver', hex: '#c0c0c0' }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} party glam outfit ${colorAnalysis.colorName} fashion`
    });
  } else if (occasion === 'date') {
    outfitSuggestions.push({
      title: `${weather || 'All Weather'} - Date Night`,
      description: `Romantic style with ${colorAnalysis.colorName} touches for date night`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: 'Soft Pink', hex: '#ffb6c1' },
        { name: 'Ivory', hex: '#fffff0' }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} date night romantic outfit ${colorAnalysis.colorName} fashion`
    });
  } else if (occasion === 'sports') {
    outfitSuggestions.push({
      title: `${weather || 'All Weather'} - Active Wear`,
      description: `Dynamic look with ${colorAnalysis.colorName} energy for sports activities`,
      colors: [
        { name: colorAnalysis.colorName, hex: colorAnalysis.original },
        { name: 'White', hex: '#ffffff' },
        { name: 'Gray', hex: '#808080' }
      ],
      pinterestLink: `https://www.pinterest.com/search/pins/?q=${weather || 'all'} athletic sport outfit ${colorAnalysis.colorName} fashion`
    });
  }

  return (
    <div className="color-analysis-page">
      <div className="top-nav">
        <button onClick={handleUserDetails} className="user-details-button">
          User Details
        </button>
        <button onClick={handleBack} className="back-button">
          ← Back
        </button>
      </div>

      <div className="main-content">
        <div className="header-section">
          <h1>Color Analysis</h1>
          <div className="context-info">
            <span className="weather-badge">{weather || 'All Weather'}</span>
            <span className="occasion-badge">{occasion || 'All Occasions'}</span>
          </div>
        </div>

        <div className="color-analysis-container">
          <div className="color-analysis-row">
            <div className="dominant-color-section">
              <h2>Dominant Color</h2>
              <div className="dominant-color-display">
                <div 
                  className="color-box large" 
                  style={{ backgroundColor: colorAnalysis.original }}
                />
              </div>
            </div>

            <div className="color-schemes-section">
              <h2>Color Schemes</h2>
              <div className="color-schemes-grid">
                <div className="color-scheme-card">
                  <h3>Complementary</h3>
                  <p>Opposite colors that create high contrast</p>
                  <div className="color-pair">
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.original }}
                    />
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.complementary }}
                    />
                  </div>
                </div>

                <div className="color-scheme-card">
                  <h3>Analogous</h3>
                  <p>Colors next to each other for harmony</p>
                  <div className="color-pair">
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.analogous1 }}
                    />
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.original }}
                    />
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.analogous2 }}
                    />
                  </div>
                </div>

                <div className="color-scheme-card">
                  <h3>Monochromatic</h3>
                  <p>Variations of the same color</p>
                  <div className="color-pair">
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.monochromatic1 }}
                    />
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.original }}
                    />
                    <div 
                      className="color-box" 
                      style={{ backgroundColor: colorAnalysis.monochromatic2 }}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="outfit-suggestions">
            <h2>Outfit Suggestions</h2>
            <div className="suggestions-grid">
              {outfitSuggestions.map((suggestion, index) => (
                <div key={index} className="suggestion-card">
                  <h3>{suggestion.title}</h3>
                  <p>{suggestion.description}</p>
                  <div className="color-pair">
                    {suggestion.colors.map((color, colorIndex) => (
                      <div 
                        key={colorIndex} 
                        className="color-box" 
                        style={{ backgroundColor: color.hex }}
                        data-color={color.name}
                      />
                    ))}
                  </div>
                  <a 
                    href={suggestion.pinterestLink} 
                    className="pinterest-link" 
                    target="_blank" 
                    rel="noopener noreferrer"
                  >
                    View Outfits
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ColorAnalysis; 