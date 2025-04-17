# model_predict.py
import timm
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import google.generativeai as genai
from report_generator import generate_report
import tempfile
import numpy as np
import base64

# --- Model Configuration ---
class_names = {
    0: "Cassava Bacterial Blight (CBB)",
    1: "Cassava Brown Streak Disease (CBSD)",
    2: "Cassava Green Mottle (CGM)",
    3: "Cassava Mosaic Disease (CMD)",
    4: "Healthy"
}

# Initialize model (must match training setup)
model = timm.create_model("rexnet_150", 
                         pretrained=False, 
                         num_classes=len(class_names))

# Load trained weights
try:
    checkpoint = torch.load("./crop_best_model.pth", 
                           map_location=torch.device('cpu'))
except FileNotFoundError:
    # Fallback paths to try
    model_paths = [
        "./crop_best_model.pth",
        "./models/crop_best_model.pth",
        "../models/crop_best_model.pth"
    ]
    
    for path in model_paths:
        try:
            checkpoint = torch.load(path, map_location=torch.device('cpu'))
            print(f"Model loaded from {path}")
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError("Could not find model file. Please ensure crop_best_model.pth exists in the correct location.")

# Clean state dict (remove DataParallel prefixes)
state_dict = {k.replace("module.", ""): v for k, v in checkpoint.items()}
model.load_state_dict(state_dict)
model.eval()

# --- Image Preprocessing ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                        std=[0.229, 0.224, 0.225])
])

def preprocess_image(image):
    # Convert to RGB (strip alpha channel if present)
    image = image.convert("RGB")
    return image
def predict_disease(image):
    try:
        # Step 1: Convert to RGB
        rgb_image = preprocess_image(image)
        
        # Step 2: Apply transforms
        img_tensor = transform(rgb_image).unsqueeze(0)
        
        # Apply transforms to the processed image
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = F.softmax(outputs, dim=1)
        
        confidence, pred_idx = torch.max(probabilities, 1)
        return class_names[pred_idx.item()], confidence.item() * 100
        
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")

# --- Gemini Integration ---
genai.configure(api_key="AIzaSyD9y4QpCzhbkhpQPbOrmhIMOfiem26IOYw")  # Replace with your key
# Using gemini-1.5-pro as it's currently the best free model available in the Gemini API
# It offers significantly improved reasoning, context handling, and multimodal capabilities
# compared to the 1.0 version while still being available in the free tier
gemini_model = genai.GenerativeModel('gemini-1.5-pro')

# model_predict.py (Updated Gemini Section)
def get_recommendation(disease_name):
    # Explicit cassava context
    if disease_name == "Healthy":
        prompt = """As a cassava agricultural expert, list:
        - 5 essential maintenance practices for healthy cassava
        - 3 early signs of disease to monitor
        - Ideal soil/weather conditions
        Format as bullet points without markdown."""
    else:
        prompt = f"""As a cassava disease specialist, create a treatment plan for {disease_name}:
        - First emergency steps
        - Approved chemical treatments (specify dosage)
        - Organic alternatives
        - Cultural control methods
        Use bullet points, avoid technical jargon."""

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3  # Lower = more factual (0-1 scale)
            )
        )
        return response.text.replace("•", "-")  # Normalize bullets
    except Exception as e:
        return f"Error generating advice: {str(e)}"

# --- Report Generation ---
def generate_full_report(image, disease, confidence, recommendation):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            image.save(tmp.name, "JPEG")
            pdf_base64 = generate_report(
                tmp.name,
                disease,
                confidence,
                recommendation
            )
        return pdf_base64
    except Exception as e:
        raise RuntimeError(f"Report generation failed: {str(e)}")