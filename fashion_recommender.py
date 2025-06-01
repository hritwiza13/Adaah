import os
import json
from PIL import Image
import numpy as np
from config import FILE_PATHS, Config
from fashion_scraper import FashionScraper

class FashionRecommender:
    def __init__(self):
        self.fashion_data = self.load_fashion_data()
        self.categories = ['tops', 'bottoms']
        self.scraper = FashionScraper()
        
    def load_fashion_data(self):
        """Load fashion data from JSON file"""
        try:
            with open(FILE_PATHS['fashion_data'], 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Fashion data file not found. Scraping new data...")
            return self.scrape_new_data()

    def scrape_new_data(self):
        """Scrape new fashion data from multiple sources"""
        # Scrape tops
        tops_data = self.scraper.scrape_all_sources('tops')
        
        # Scrape bottoms
        bottoms_data = self.scraper.scrape_all_sources('bottoms')
        
        # Combine and save data
        all_data = tops_data + bottoms_data
        self.scraper.data = all_data
        self.scraper.save_to_json()
        
        return all_data

    def validate_image(self, image_path):
        """Validate uploaded image"""
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return False, "File does not exist"
            
            # Check file extension
            ext = os.path.splitext(image_path)[1].lower()
            if ext not in Config.ALLOWED_EXTENSIONS:
                return False, f"Invalid file extension. Allowed extensions: {Config.ALLOWED_EXTENSIONS}"
            
            # Check file size
            if os.path.getsize(image_path) > Config.MAX_CONTENT_LENGTH:
                return False, f"File too large. Maximum size: {Config.MAX_CONTENT_LENGTH/1024/1024}MB"
            
            # Validate image format
            try:
                with Image.open(image_path) as img:
                    img.verify()
                return True, "Image is valid"
            except Exception as e:
                return False, f"Invalid image format: {str(e)}"
                
        except Exception as e:
            return False, f"Error validating image: {str(e)}"

    def get_recommendations(self, image_path, category):
        """Get fashion recommendations based on uploaded image"""
        # Validate image
        is_valid, message = self.validate_image(image_path)
        if not is_valid:
            return {"error": message}
        
        # Validate category
        if category not in self.categories:
            return {"error": f"Invalid category. Must be one of: {self.categories}"}
        
        # Get recommendations based on category
        if category == 'tops':
            return self.get_bottom_recommendations(image_path)
        else:  # bottoms
            return self.get_top_recommendations(image_path)

    def get_bottom_recommendations(self, top_image_path):
        """Get bottom recommendations based on top image"""
        # Scrape new bottom recommendations
        bottoms_data = self.scraper.scrape_all_sources('bottoms')
        
        recommendations = []
        for item in bottoms_data:
            recommendations.append({
                'image_url': item['image_url'],
                'title': item['title'],
                'description': f"Brand: {item['brand']} | Price: {item['price']}",
                'fashion_details': {
                    'category': item['category'],
                    'brand': item['brand'],
                    'price': item['price'],
                    'source': item['source']
                }
            })
        
        return {
            'status': 'success',
            'message': 'Found bottom recommendations for your top',
            'recommendations': recommendations
        }

    def get_top_recommendations(self, bottom_image_path):
        """Get top recommendations based on bottom image"""
        # Scrape new top recommendations
        tops_data = self.scraper.scrape_all_sources('tops')
        
        recommendations = []
        for item in tops_data:
            recommendations.append({
                'image_url': item['image_url'],
                'title': item['title'],
                'description': f"Brand: {item['brand']} | Price: {item['price']}",
                'fashion_details': {
                    'category': item['category'],
                    'brand': item['brand'],
                    'price': item['price'],
                    'source': item['source']
                }
            })
        
        return {
            'status': 'success',
            'message': 'Found top recommendations for your bottom',
            'recommendations': recommendations
        }

# Example usage
if __name__ == "__main__":
    # Initialize recommender
    recommender = FashionRecommender()
    
    # Example: Get recommendations for a top
    top_image_path = "path/to/your/top/image.jpg"
    recommendations = recommender.get_recommendations(top_image_path, 'tops')
    print(json.dumps(recommendations, indent=4)) 