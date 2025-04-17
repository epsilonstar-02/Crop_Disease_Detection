from flask import Flask, request, jsonify
from model_predict import predict_disease, get_recommendation, preprocess_image
from PIL import Image
import torch
import os

app = Flask(__name__)

# Configure CORS if needed
# from flask_cors import CORS
# CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    try:
        # Open and preprocess the image
        image = Image.open(image_file)
        
        # Get the disease prediction
        disease = predict_disease(image)
        
        # Get treatment recommendations using Gemini AI
        recommendation = get_recommendation(disease)
        
        # Return the results
        return jsonify({
            "disease": disease,
            "recommendation": recommendation,
            "confidence": "high"  # This could be dynamically set based on model output
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": True})

if __name__ == '__main__':
    # Ensure CUDA is available if using PyTorch with GPU
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU for inference.")
    else:
        print("CUDA not available. Using CPU for inference.")
    
    app.run(debug=True, port=5000, host='0.0.0.0')