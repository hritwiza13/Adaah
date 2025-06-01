import axios from 'axios';
import config from '../config';

const api = axios.create({
    baseURL: config.API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadImage = async (file, category, gender) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('gender', gender);
    
    try {
        const response = await api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const recommendOutfit = async (preferences, weather) => {
    try {
        const response = await api.post('/api/recommend-outfit', {
            preferences,
            weather,
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const analyzeStyle = async (imageFile) => {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    try {
        const response = await api.post('/api/analyze-style', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const virtualTryOn = async (userImage, clothingImage) => {
    const formData = new FormData();
    formData.append('user_image', userImage);
    formData.append('clothing_image', clothingImage);
    
    try {
        const response = await api.post('/api/virtual-tryon', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const getSeasonalWardrobe = async (season, userId) => {
    try {
        const response = await api.post('/api/seasonal-wardrobe', {
            season,
            user_id: userId,
        });
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
};

export const checkHealth = async () => {
    try {
        const response = await api.get('/api/health');
        return response.data;
    } catch (error) {
        throw error.response?.data || error.message;
    }
}; 