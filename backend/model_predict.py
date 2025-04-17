import torch
import numpy as np
from PIL import Image
import json
import pandas as pd
import google.generativeai as genai

# Load your pre-trained model (PyTorch model since it's a .pth file)
model = torch.load("F:\ML_projects\Crop-Disease Detection\backend\crop_best_model.pth")
model.eval()  # Set the model to evaluation mode

# Load label mappings (adjust based on your dataset's JSON/CSV)
class_names = {
    0: "Cassava Bacterial Blight (CBB)",
    1: "Cassava Brown Streak Disease (CBSD)",
    2: "Cassava Green Mottle (CGM)",
    3: "Cassava Mosaic Disease (CMD)",
    4: "Healthy"
}

# Configure Gemini
genai.configure(api_key="YOUR_API_KEY")
model_genai = genai.GenerativeModel('gemini-pro')

def preprocess_image(image):
    # Resize and normalize the image (adjust to match model's expected input)
    image = image.resize((224, 224))  # example size
    # Convert to tensor and normalize according to PyTorch conventions
    image_tensor = torch.from_numpy(np.array(image).transpose((2, 0, 1))).float() / 255.0
    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)
    return image_tensor

def predict_disease(image):
    processed_image = preprocess_image(image)
    # Move tensor to the same device as the model
    device = next(model.parameters()).device
    processed_image = processed_image.to(device)
    
    with torch.no_grad():
        prediction = model(processed_image)
    
    # Get the predicted class
    predicted_class = torch.argmax(prediction, dim=1).item()
    disease = class_names[predicted_class]
    return disease

def get_recommendation(disease_name):
    prompt = f"""
    As an agricultural expert, provide a concise, bullet-pointed treatment plan for {disease_name} in cassava.
    Include:
    - Immediate actions
    - Long-term prevention
    - Approved chemicals/organic remedies
    Avoid markdown formatting.
    Provide only scientifically validated methods.
    """
    try:
        response = model_genai.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Recommendation unavailable. Error: {str(e)}"