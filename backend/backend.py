from flask import Flask, request, jsonify
from model_predict import predict_disease, get_recommendation, generate_full_report
from PIL import Image
import os
from flask_cors import CORS

# Ensure directories exist for temporary files
os.makedirs('temp', exist_ok=True)


app = Flask(__name__)

# Enable CORS
CORS(app)

# Update the predict() function
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    try:
        image = Image.open(image_file)
        disease, confidence = predict_disease(image)
        recommendation = get_recommendation(disease)
        pdf_base64 = generate_full_report(image, disease, confidence, recommendation)
        
        return jsonify({
            "disease": disease,
            "confidence": confidence,
            "recommendation": recommendation,
            "pdf": pdf_base64  # Base64-encoded PDF
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "model_loaded": True})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, port=5000, host='0.0.0.0')