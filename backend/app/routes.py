# routes.py
from flask import request, jsonify, Blueprint
from PIL import Image
import io
import os
from backend.app.model import model_instance

api = Blueprint('api', __name__)

@api.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint for disease prediction
    
    Expects: 
        - An image file with field name 'image'
        
    Returns:
        - JSON with disease, confidence, recommendation, and PDF report
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    try:
        try:
            image = Image.open(image_file.stream)
            image.verify()
            image_file.stream.seek(0)
            image = Image.open(image_file.stream)
        except Exception as e:
            return jsonify({"error": f"Invalid image file: {str(e)}"}), 400
        
        disease, confidence = model_instance.predict(image)
        
        recommendation = model_instance.get_recommendation(disease)
        
        try:
            pdf_base64 = model_instance.generate_full_report(image, disease, confidence, recommendation)
        except Exception as e:
            print(f"PDF generation failed: {str(e)}")
            return jsonify({
                "disease": disease,
                "confidence": confidence,
                "recommendation": recommendation,
                "pdf": None,
                "pdf_error": f"Could not generate PDF: {str(e)}"
            })
        
        return jsonify({
            "disease": disease,
            "confidence": confidence,
            "recommendation": recommendation,
            "pdf": pdf_base64
        })
    except Exception as e:
        import traceback
        print(f"Prediction error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model_loaded": model_instance.model is not None}) 