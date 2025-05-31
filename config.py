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

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 