# Fashion AI Backend

A Flask-based backend for a fashion application featuring personalized outfit recommendations, style analysis, virtual try-on technology, and seasonal wardrobe planning.

## Features

- **Personalized Outfit Recommendations**: Get outfit suggestions based on user preferences and weather conditions
- **Style Analysis & Trend Detection**: Analyze clothing images to detect styles and current trends
- **Virtual Try-on Technology**: Try clothes virtually using AI-powered image processing
- **Seasonal Wardrobe Planning**: Get seasonal wardrobe recommendations and planning assistance

## Technologies Used

- Python 3.8+
- Flask
- TensorFlow
- OpenCV
- NumPy
- Pillow
- scikit-learn

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
STYLE_MODEL_PATH=models/style_model.h5
VIRTUAL_TRYON_MODEL_PATH=models/virtual_tryon.h5
UPLOAD_FOLDER=uploads
RESULT_FOLDER=static/tryon_results
```

4. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Outfit Recommendations
- **POST** `/api/recommend-outfit`
  - Request body: `{ "preferences": {}, "weather": {} }`
  - Returns personalized outfit recommendations

### Style Analysis
- **POST** `/api/analyze-style`
  - Request: Form data with image file
  - Returns style analysis and trend detection results

### Virtual Try-on
- **POST** `/api/virtual-tryon`
  - Request: Form data with user image and clothing image
  - Returns virtual try-on result

### Seasonal Wardrobe
- **POST** `/api/seasonal-wardrobe`
  - Request body: `{ "season": "summer", "user_id": "123" }`
  - Returns seasonal wardrobe recommendations

## Project Structure

```
.
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── requirements.txt    # Project dependencies
├── utils/
│   └── ml_utils.py     # Machine learning utilities
├── models/            # ML model files
├── uploads/           # Uploaded images
└── static/
    └── tryon_results/ # Virtual try-on results
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
