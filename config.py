import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Model paths
    STYLE_MODEL_PATH = os.getenv('STYLE_MODEL_PATH', 'models/style_model.h5')
    VIRTUAL_TRYON_MODEL_PATH = os.getenv('VIRTUAL_TRYON_MODEL_PATH', 'models/virtual_tryon.h5')
    
    # API settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Storage settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    RESULT_FOLDER = os.getenv('RESULT_FOLDER', 'static/tryon_results')
    
    # ML settings
    IMAGE_SIZE = (224, 224)
    BATCH_SIZE = 32
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.RESULT_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

# Base URLs
BASE_URL = "http://localhost:10000"  # Based on your render.yaml PORT setting

# API Endpoints
API_ENDPOINTS = {
    'recommend_outfit': f"{BASE_URL}/api/recommend-outfit",
    'health_check': f"{BASE_URL}/api/recommend-outfit",  # Based on your render.yaml healthCheckPath
    'fashion_trends': f"{BASE_URL}/api/fashion-trends",
    'outfit_suggestions': f"{BASE_URL}/api/outfit-suggestions"
}

# Pinterest Scraping URLs
PINTEREST_URLS = {
    'women': {
        'trends': "https://www.pinterest.com/search/pins/?q=womens+fashion+trends+2024",
        'outfits': "https://www.pinterest.com/search/pins/?q=womens+outfit+ideas",
        'dresses': "https://www.pinterest.com/search/pins/?q=womens+dresses",
        'casual': "https://www.pinterest.com/search/pins/?q=womens+casual+outfits",
        'formal': "https://www.pinterest.com/search/pins/?q=womens+formal+wear",
        'summer': "https://www.pinterest.com/search/pins/?q=womens+summer+fashion",
        'winter': "https://www.pinterest.com/search/pins/?q=womens+winter+fashion"
    },
    'men': {
        'trends': "https://www.pinterest.com/search/pins/?q=mens+fashion+trends+2024",
        'outfits': "https://www.pinterest.com/search/pins/?q=mens+outfit+ideas",
        'casual': "https://www.pinterest.com/search/pins/?q=mens+casual+outfits",
        'formal': "https://www.pinterest.com/search/pins/?q=mens+formal+wear",
        'summer': "https://www.pinterest.com/search/pins/?q=mens+summer+fashion",
        'winter': "https://www.pinterest.com/search/pins/?q=mens+winter+fashion"
    }
}

# Model Paths (from render.yaml)
MODEL_PATHS = {
    'style_model': "models/style_model.h5",
    'virtual_tryon': "models/virtual_tryon.h5"
}

# Scraping Settings
SCRAPING_SETTINGS = {
    'max_pages': 5,
    'scroll_pages': 5,
    'headless': True,
    'timeout': 10,
    'delay': 2
}

# File Paths
FILE_PATHS = {
    'fashion_data': 'data/fashion_data.json',
    'trends_data': 'data/trends_data.json',
    'images_folder': 'static/images/fashion'
}

# Environment Variables (from render.yaml)
ENV_VARS = {
    'PYTHON_VERSION': '3.9.0',
    'FLASK_DEBUG': 'False',
    'FLASK_ENV': 'production',
    'PORT': '10000'
}

# API Settings
API_SETTINGS = {
    'workers': 2,
    'threads': 4,
    'timeout': 180,
    'max_requests': 1000,
    'max_requests_jitter': 50,
    'log_level': 'info'
}

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 