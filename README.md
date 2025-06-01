# Fashion Recommendation System

A web-based fashion recommendation system that suggests matching clothing items based on uploaded images. The system scrapes real-time fashion data from multiple sources (ASOS, H&M, and Zara) to provide up-to-date recommendations.

## Features

- Image upload for tops and bottoms
- Real-time fashion data scraping from multiple sources
- Price and brand information
- Responsive web interface
- Automatic image validation
- Multi-source recommendations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fashion-recommender
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:10000
```

3. Upload an image:
   - Select category (tops or bottoms)
   - Choose an image file
   - Click "Get Recommendations"

## Project Structure

```
fashion-recommender/
├── app.py                 # Flask application
├── config.py             # Configuration settings
├── fashion_scraper.py    # Multi-source web scraper
├── fashion_recommender.py # Recommendation engine
├── requirements.txt      # Project dependencies
├── static/              # Static files
│   └── images/         # Downloaded images
├── templates/          # HTML templates
│   └── index.html     # Main interface
└── data/              # Scraped data
```

## Dependencies

- Flask
- BeautifulSoup4
- Requests
- Pillow
- Python-dotenv

## Configuration

The system can be configured through `config.py`:

- Scraping settings (timeouts, delays)
- File paths
- API endpoints
- Environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
