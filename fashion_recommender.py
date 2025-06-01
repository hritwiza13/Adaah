import os
import json
from PIL import Image
import numpy as np
from config import FILE_PATHS, Config
from fashion_scraper import FashionScraper
import colorsys
import requests
from io import BytesIO

class FashionRecommender:
    def __init__(self):
        print("FashionRecommender: __init__ started") # Debug print
        
        print("FashionRecommender: Initializing scraper...") # Debug print
        # Initialize the FashionScraper
        self.scraper = FashionScraper()
        print("FashionRecommender: Scraper initialized.") # Debug print

        self.fashion_data = self.load_fashion_data()
        self.categories = ['tops', 'bottoms']

    def load_fashion_data(self):
        """Load fashion data from JSON file"""
        print("FashionRecommender: load_fashion_data started") # Debug print
        try:
            with open(FILE_PATHS['fashion_data'], 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("FashionRecommender: Fashion data file not found. Scraping new data...") # Debug print
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

    def extract_dominant_color(self, image_path, palette_size=10):
        """Extracts the dominant color from an image, excluding white, black, and near-white/black colors."""
        try:
            # Handle both file paths and PIL Image objects
            if isinstance(image_path, str):
                img = Image.open(image_path).convert("RGBA")
            elif isinstance(image_path, Image.Image):
                img = image_path.convert("RGBA")
            else:
                return None # Invalid input
                
            # Reduce the image to a palette
            # Resize for faster processing, but keep a reasonable size
            img.thumbnail((150, 150))
            paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

            # Get the palette and counts
            palette = paletted.getpalette()
            color_counts = sorted(paletted.getcolors(), reverse=True)

            # Extract dominant color, excluding white, black, and near-white/black
            for count, index in color_counts:
                # Palette is a list of RGB values [R1, G1, B1, R2, G2, B2, ...]
                r, g, b = palette[index * 3:index * 3 + 3]
                
                # Calculate brightness (sum of RGB values)
                brightness = r + g + b
                
                # Check if color is close to white (brightness > 700) or black (brightness < 50)
                # Adjust thresholds as needed
                if not (brightness > 700 or brightness < 50):
                     # Return color in HSV for potentially better comparison later
                    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
                    return {'rgb': f'rgb({r}, {g}, {b})', 'hsv': (h, s, v)}

            # If only white, black, or near colors found, return a neutral grey
            r, g, b = 128, 128, 128
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            return {'rgb': f'rgb({r}, {g}, {b})', 'hsv': (h, s, v)}

        except Exception as e:
            print(f"Error extracting dominant color: {e}")
            return None

    def get_color_similarity(self, color1_info, color2_info, h_tolerance=0.1, s_v_tolerance=0.2):
        """Calculates color similarity between two colors in HSV space."""
        if not color1_info or not color2_info:
            return False

        try:
            h1, s1, v1 = color1_info['hsv']
            h2, s2, v2 = color2_info['hsv']
            
            # Calculate hue difference (handle wrap-around)
            hue_diff = min(abs(h1 - h2), 1 - abs(h1 - h2))
            
            # Calculate saturation and value differences
            s_diff = abs(s1 - s2)
            v_diff = abs(v1 - v2)

            # Check if colors are similar based on tolerances
            return hue_diff < h_tolerance and s_diff < s_v_tolerance and v_diff < s_v_tolerance

        except Exception as e:
            print(f"Error calculating color similarity: {e}")
            return False

    def get_recommendations(self, image_path, category, gender):
        """Get fashion recommendations based on uploaded image and gender"""
        # Validate image
        is_valid, message = self.validate_image(image_path)
        if not is_valid:
            return {"error": message}
        
        # Validate category
        if category not in self.categories:
            return {"error": f"Invalid category. Must be one of: {self.categories}"}
        
        # Validate gender
        if gender not in ['men', 'women']:
            return {"error": "Invalid gender specified. Must be 'men' or 'women'."}

        # Get recommendations based on category and gender
        if category == 'tops':
            return self.get_bottom_recommendations(image_path, gender)
        else:  # bottoms
            return self.get_top_recommendations(image_path, gender)

    def filter_by_gender(self, items, gender):
        """Filters a list of fashion items by gender based on keywords."""
        filtered_items = []
        # Define keywords for gender detection (can be expanded)
        men_keywords = ['men', 'male', 'guy']
        women_keywords = ['women', 'female', 'girl']
        
        target_keywords = men_keywords if gender == 'men' else women_keywords

        for item in items:
            # Check if title or description contains gender-specific keywords
            if any(keyword in item['title'].lower() for keyword in target_keywords) or \
               (item.get('description') and any(keyword in item['description'].lower() for keyword in target_keywords)):
                filtered_items.append(item)
                
        # If no specific gender items found, return a limited number of general items
        if not filtered_items:
            print(f"No {gender} specific items found. Returning a few general items.")
            return items[:10] # Return first 10 items as a fallback

        return filtered_items

    def get_bottom_recommendations(self, top_image_path, gender):
        """Get bottom recommendations based on top image and gender"""
        # Scrape new bottom recommendations
        bottoms_data = self.scraper.scrape_all_sources('bottoms')
        
        # Filter data by gender
        filtered_bottoms = self.filter_by_gender(bottoms_data, gender)

        recommendations = []
        
        # Extract dominant color from the top image
        dominant_top_color_info = self.extract_dominant_color(top_image_path)
        
        print(f"Dominant color of uploaded top: {dominant_top_color_info}") # Debugging print

        if dominant_top_color_info:
            for item in filtered_bottoms:
                if item['image_url']:
                    try:
                        # Download scraped item image
                        response = requests.get(item['image_url'], timeout=Config.REQUEST_TIMEOUT)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            # Extract dominant color from scraped item image
                            dominant_item_color_info = self.extract_dominant_color(img)
                            
                            print(f"  Comparing with item {item['title']}: {dominant_item_color_info}") # Debugging print

                            # Check for color similarity
                            if dominant_item_color_info and self.get_color_similarity(dominant_top_color_info, dominant_item_color_info):
                                recommendations.append({
                                    'image_url': item['image_url'],
                                    'title': item['title'],
                                    'description': f"Brand: {item['brand']} | Price: {item['price']}",
                                    'fashion_details': {
                                        'category': item['category'],
                                        'brand': item['brand'],
                                        'price': item['price'],
                                        'source': item['source'],
                                        'color': dominant_item_color_info['rgb'] # Add detected color (RGB string)
                                    }
                                })
                    except Exception as e:
                        print(f"Error processing image for {item['title']}: {e}")

        # If no color matches found or color extraction failed, return all scraped bottoms (filtered by gender) as a fallback
        if not recommendations:
             for item in filtered_bottoms:
                recommendations.append({
                    'image_url': item['image_url'],
                    'title': item['title'],
                    'description': f"Brand: {item['brand']} | Price: {item['price']}",
                    'fashion_details': {
                        'category': item['category'],
                        'brand': item['brand'],
                        'price': item['price'],
                        'source': item['source'],
                        'color': 'N/A' # Indicate color wasn't matched
                    }
                })

        return {
            'status': 'success',
            'message': f'Found {gender} bottom recommendations for your top',
            'recommendations': recommendations
        }

    def get_top_recommendations(self, bottom_image_path, gender):
        """Get top recommendations based on bottom image and gender"""
        # Scrape new top recommendations
        tops_data = self.scraper.scrape_all_sources('tops')
        
        # Filter data by gender
        filtered_tops = self.filter_by_gender(tops_data, gender)

        recommendations = []

        # Extract dominant color from the bottom image
        dominant_bottom_color_info = self.extract_dominant_color(bottom_image_path)

        print(f"Dominant color of uploaded bottom: {dominant_bottom_color_info}") # Debugging print

        if dominant_bottom_color_info:
            for item in filtered_tops:
                if item['image_url']:
                    try:
                        # Download scraped item image
                        response = requests.get(item['image_url'], timeout=Config.REQUEST_TIMEOUT)
                        if response.status_code == 200:
                            img = Image.open(BytesIO(response.content))
                            # Extract dominant color from scraped item image
                            dominant_item_color_info = self.extract_dominant_color(img)

                            print(f"  Comparing with item {item['title']}: {dominant_item_color_info}") # Debugging print

                            # Check for color similarity
                            if dominant_item_color_info and self.get_color_similarity(dominant_bottom_color_info, dominant_item_color_info):
                                recommendations.append({
                                    'image_url': item['image_url'],
                                    'title': item['title'],
                                    'description': f"Brand: {item['brand']} | Price: {item['price']}",
                                    'fashion_details': {
                                        'category': item['category'],
                                        'brand': item['brand'],
                                        'price': item['price'],
                                        'source': item['source'],
                                        'color': dominant_item_color_info['rgb'] # Add detected color (RGB string)
                                    }
                                })
                    except Exception as e:
                        print(f"Error processing image for {item['title']}: {e}")

        # If no color matches found or color extraction failed, return all scraped tops (filtered by gender) as a fallback
        if not recommendations:
             for item in filtered_tops:
                recommendations.append({
                    'image_url': item['image_url'],
                    'title': item['title'],
                    'description': f"Brand: {item['brand']} | Price: {item['price']}",
                    'fashion_details': {
                        'category': item['category'],
                        'brand': item['brand'],
                        'price': item['price'],
                        'source': item['source'],
                        'color': 'N/A' # Indicate color wasn't matched
                    }
                })

        return {
            'status': 'success',
            'message': f'Found {gender} top recommendations for your bottom',
            'recommendations': recommendations
        }

# Example usage
if __name__ == "__main__":
    # Initialize recommender
    recommender = FashionRecommender()
    
    # Example: Get recommendations for a top
    top_image_path = "path/to/your/top/image.jpg"
    
    # Example of using the new color extraction method
    # dominant_color = recommender.extract_dominant_color(top_image_path)
    # print(f"Dominant color: {dominant_color}")

    # recommendations = recommender.get_recommendations(top_image_path, 'tops', 'men')
    # print(json.dumps(recommendations, indent=4)) 