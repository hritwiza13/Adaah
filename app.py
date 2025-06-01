from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image
import io
import json
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from fashion_recommender import FashionRecommender
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Configure for production
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Load pre-trained models (to be implemented)
# style_model = tf.keras.models.load_model('models/style_model.h5')
# virtual_tryon_model = tf.keras.models.load_model('models/virtual_tryon.h5')

# Initialize the fashion recommender
recommender = FashionRecommender()

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    category = request.form.get('category')
    gender = request.form.get('gender') # Get gender from form data
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Get recommendations
            # Pass the gender to the recommender
            recommendations_data = recommender.get_recommendations(filepath, category, gender=gender)
            
            # Clean up the uploaded file
            os.remove(filepath)
            
            if 'error' in recommendations_data:
                return jsonify(recommendations_data), 400

            return jsonify(recommendations_data), 200
            
        except Exception as e:
            # Clean up the uploaded file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/recommend-outfit', methods=['POST'])
def recommend_outfit():
    try:
        data = request.json
        user_preferences = data.get('preferences', {})
        weather_data = data.get('weather', {})
        
        # Implement outfit recommendation logic
        recommendations = {
            'outfits': [
                {
                    'id': 1,
                    'items': ['t-shirt', 'jeans', 'sneakers'],
                    'confidence': 0.85,
                    'style': 'casual'
                }
            ]
        }
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-style', methods=['POST'])
def analyze_style():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
            
        image_file = request.files['image']
        image = Image.open(image_file)
        
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Implement style analysis logic
        style_analysis = {
            'dominant_colors': ['#FF0000', '#0000FF'],
            'style_category': 'casual',
            'confidence': 0.92,
            'trends': ['minimalist', 'streetwear']
        }
        
        return jsonify(style_analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/virtual-tryon', methods=['POST'])
def virtual_tryon():
    try:
        if 'user_image' not in request.files or 'clothing_image' not in request.files:
            return jsonify({'error': 'Both user image and clothing image are required'}), 400
            
        user_image = request.files['user_image']
        clothing_image = request.files['clothing_image']
        
        # Implement virtual try-on logic
        result = {
            'success': True,
            'result_image_url': '/static/tryon_results/result.jpg',
            'confidence': 0.88
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/seasonal-wardrobe', methods=['POST'])
def seasonal_wardrobe():
    try:
        data = request.json
        season = data.get('season', 'summer')
        user_id = data.get('user_id')
        
        # Implement seasonal wardrobe planning logic
        wardrobe_plan = {
            'season': season,
            'recommended_items': [
                {
                    'category': 'tops',
                    'items': ['t-shirts', 'blouses', 'tank tops'],
                    'quantity': 5
                },
                {
                    'category': 'bottoms',
                    'items': ['shorts', 'skirts', 'light pants'],
                    'quantity': 4
                }
            ],
            'color_palette': ['#FFD700', '#87CEEB', '#FF69B4']
        }
        
        return jsonify(wardrobe_plan)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 