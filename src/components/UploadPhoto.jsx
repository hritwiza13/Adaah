import { useState } from "react"
import { useNavigate } from "react-router"
import "./uploadPhoto.css"

const UploadPhoto = () => {
  const navigate = useNavigate()
  const [file, setFile] = useState(null)
  const [weather, setweather] = useState("")
  const [occasion, setOccasion] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [dominantColor, setDominantColor] = useState("")
  const [colorAnalysis, setColorAnalysis] = useState(null)
  const [colorRecommendations, setColorRecommendations] = useState(null)

  // Get user name from localStorage
  const userName = window.localStorage.getItem('user_name') || '';

  const getDominantColor = (imageFile) => {
    return new Promise((resolve) => {
      const img = new Image()
      const canvas = document.createElement('canvas')
      const ctx = canvas.getContext('2d')
      
      img.onload = () => {
        // Resize image for better performance while maintaining accuracy
        const maxSize = 150
        let width = img.width
        let height = img.height
        
        if (width > height && width > maxSize) {
          height = Math.round((height * maxSize) / width)
          width = maxSize
        } else if (height > maxSize) {
          width = Math.round((width * maxSize) / height)
          height = maxSize
        }
        
        canvas.width = width
        canvas.height = height
        ctx.drawImage(img, 0, 0, width, height)
        
        const imageData = ctx.getImageData(0, 0, width, height).data
        const colorCounts = {}
        const totalPixels = width * height
        
        // Group similar colors together
        for (let i = 0; i < imageData.length; i += 4) {
          const r = Math.round(imageData[i] / 10) * 10
          const g = Math.round(imageData[i + 1] / 10) * 10
          const b = Math.round(imageData[i + 2] / 10) * 10
          const color = `rgb(${r},${g},${b})`
          colorCounts[color] = (colorCounts[color] || 0) + 1
        }
        
        // Find the most dominant color
        const dominantColor = Object.entries(colorCounts)
          .sort(([,a], [,b]) => b - a)[0][0]
        
        // Calculate color percentages
        const colorPercentages = Object.entries(colorCounts)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 5)
          .map(([color, count]) => ({
            color,
            percentage: Math.round((count / totalPixels) * 100)
          }))
        
        resolve({ dominantColor, colorPercentages })
      }
      
      img.src = URL.createObjectURL(imageFile)
    })
  }

  const analyzeColor = (rgbColor) => {
    const [r, g, b] = rgbColor.match(/\d+/g).map(Number)
    
    // Convert RGB to HSL for better color analysis
    const [h, s, l] = rgbToHsl(r, g, b)
    
    // Determine color characteristics
    const brightness = (r * 299 + g * 587 + b * 114) / 1000
    const isWarm = h >= 0 && h <= 60 || h >= 300
    const saturation = s * 100
    const lightness = l * 100
    
    // Get exact color name
    const colorName = getExactColorName(r, g, b)
    
    // Get complementary color
    const complementary = getComplementaryColor(h, s, l)
    
    // Get analogous colors
    const [analogous1, analogous2] = getAnalogousColors(h, s, l)

    // Get triadic colors
    const triadic1 = hslToRgb(((h + 120) % 360) / 360, s, l)
    const triadic2 = hslToRgb(((h + 240) % 360) / 360, s, l)

    // Get split-complementary colors
    const splitComp1 = hslToRgb(((h + 150) % 360) / 360, s, l)
    const splitComp2 = hslToRgb(((h + 210) % 360) / 360, s, l)

    // Get monochromatic variations
    const monochromatic1 = hslToRgb(h / 360, Math.min(s + 0.2, 1), l)
    const monochromatic2 = hslToRgb(h / 360, Math.max(s - 0.2, 0), l)
    
    return {
      original: rgbColor,
      hex: rgbToHex(r, g, b),
      hsl: { h, s, l },
      brightness,
      isWarm,
      saturation,
      lightness,
      colorName,
      complementary,
      analogous1,
      analogous2,
      triadic1,
      triadic2,
      splitComp1,
      splitComp2,
      monochromatic1,
      monochromatic2
    }
  }

  const rgbToHsl = (r, g, b) => {
    r /= 255
    g /= 255
    b /= 255
    
    const max = Math.max(r, g, b)
    const min = Math.min(r, g, b)
    let h, s, l = (max + min) / 2
    
    if (max === min) {
      h = s = 0
    } else {
      const d = max - min
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
      
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break
        case g: h = (b - r) / d + 2; break
        case b: h = (r - g) / d + 4; break
      }
      
      h /= 6
    }
    
    return [h * 360, s, l]
  }

  const rgbToHex = (r, g, b) => {
    return '#' + [r, g, b].map(x => {
      const hex = x.toString(16)
      return hex.length === 1 ? '0' + hex : hex
    }).join('')
  }

  const getExactColorName = (r, g, b) => {
    // This is a simplified version - you can expand this with more color names
    const colors = {
      'red': [255, 0, 0],
      'crimson': [220, 20, 60],
      'maroon': [128, 0, 0],
      'pink': [255, 192, 203],
      'orange': [255, 165, 0],
      'yellow': [255, 255, 0],
      'green': [0, 128, 0],
      'teal': [0, 128, 128],
      'blue': [0, 0, 255],
      'navy': [0, 0, 128],
      'purple': [128, 0, 128],
      'violet': [238, 130, 238],
      'brown': [165, 42, 42],
      'beige': [245, 245, 220],
      'white': [255, 255, 255],
      'gray': [128, 128, 128],
      'black': [0, 0, 0]
    }
    
    let closestColor = ''
    let minDistance = Infinity
    
    for (const [name, [cr, cg, cb]] of Object.entries(colors)) {
      const distance = Math.sqrt(
        Math.pow(r - cr, 2) +
        Math.pow(g - cg, 2) +
        Math.pow(b - cb, 2)
      )
      
      if (distance < minDistance) {
        minDistance = distance
        closestColor = name
      }
    }
    
    return closestColor
  }

  const getComplementaryColor = (h, s, l) => {
    const newH = (h + 180) % 360
    return hslToRgb(newH / 360, s, l)
  }

  const getAnalogousColors = (h, s, l) => {
    const color1 = hslToRgb(((h + 30) % 360) / 360, s, l)
    const color2 = hslToRgb(((h - 30 + 360) % 360) / 360, s, l)
    return [color1, color2]
  }

  const hslToRgb = (h, s, l) => {
    let r, g, b
    
    if (s === 0) {
      r = g = b = l
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1
        if (t > 1) t -= 1
        if (t < 1/6) return p + (q - p) * 6 * t
        if (t < 1/2) return q
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6
        return p
      }
      
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s
      const p = 2 * l - q
      
      r = hue2rgb(p, q, h + 1/3)
      g = hue2rgb(p, q, h)
      b = hue2rgb(p, q, h - 1/3)
    }
    
    return `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`
  }

  const handleFileChange = async (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      setFile(selectedFile)
      const { dominantColor, colorPercentages } = await getDominantColor(selectedFile)
      setDominantColor(dominantColor)
      const analysis = analyzeColor(dominantColor)
      setColorAnalysis({ ...analysis, colorPercentages })
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")

    if (!file) {
      setError("Please upload an image")
      setLoading(false)
      return
    }

    if (!weather || !occasion || !colorAnalysis) {
      setError("Please select both weather and occasion")
      setLoading(false)
      return
    }

    // Prepare color data for the next page
    const colorData = {
      original: colorAnalysis.original,
      colorName: colorAnalysis.colorName,
      complementary: colorAnalysis.complementary,
      analogous1: colorAnalysis.analogous1,
      analogous2: colorAnalysis.analogous2,
      triadic1: colorAnalysis.triadic1,
      triadic2: colorAnalysis.triadic2,
      splitComp1: colorAnalysis.splitComp1,
      splitComp2: colorAnalysis.splitComp2,
      monochromatic1: colorAnalysis.monochromatic1,
      monochromatic2: colorAnalysis.monochromatic2
    }

    // Navigate to results page with the color analysis data
    navigate('/results', {
      state: {
        colorAnalysis: colorData,
        weather,
        occasion
      }
    })
    setLoading(false)
  }

  const handleLogin = () => {
    navigate("/login")
  }

  const handleSignup = () => {
    navigate("/signup")
  }

  return (
    <div className="whole">
      <div className="top-nav">
      </div>

      <div className="app-container">
        <div className="right-panel">
          <div className="welcome-section">
            {userName && (
              <div className="user-greeting" style={{ fontWeight: 600, fontSize: '1.1rem', color: '#4d0101', marginBottom: '10px' }}>
                Welcome, {userName}!
              </div>
            )}
            <h2 className="welcome-title">
              Welcome to Adaah <span className="heart-emoji">💗</span>
            </h2>

            <div className="file-upload-container">
              <label htmlFor="file-upload" className="file-upload-label">
                {file ? file.name : "Upload your image"}
              </label>
              <input
                id="file-upload"
                type="file"
                className="file-upload-input"
                onChange={handleFileChange}
                accept="image/*"
              />
            </div>

            {/* Quick Color Preview section removed as per user request */}

            <div className="filters-container">
              <div className="dropdown-left">
                <select
                  id="weather-select"
                  className="dropdown-button"
                  value={weather}
                  onChange={(e) => setweather(e.target.value)}
                >
                  <option value="" disabled>Select Weather</option>
                  <option value="Summer">Summer</option>
                  <option value="Spring">Spring</option>
                  <option value="Rainy">Rainy</option>
                  <option value="Fall">Fall</option>
                  <option value="Winter">Winter</option>
                </select>
              </div>

              <div className="dropdown-right">
                <select
                  id="occasion-select"
                  className="dropdown-button"
                  value={occasion}
                  onChange={(e) => setOccasion(e.target.value)}
                >
                  <option value="" disabled>Select Occasion</option>
                  <option value="Casual">Casual</option>
                  <option value="Formal">Formal</option>
                  <option value="Party">Party</option>
                  <option value="Festive">Festive</option>
                  <option value="Work">Work</option>
                </select>
              </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              className="get-look-button"
              onClick={handleSubmit}
              disabled={loading}
            >
              <span className="sparkle">✨</span>{" "}
              {loading ? "Processing..." : "Wait for the Magic!"}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadPhoto
