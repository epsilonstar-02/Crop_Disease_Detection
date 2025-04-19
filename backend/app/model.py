# model.py
import timm
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import google.generativeai as genai
import tempfile
import os
from pathlib import Path
from datetime import datetime

from backend.utils.config import MODEL_PATH, GEMINI_API_KEY, TEMP_DIR
from backend.utils.report_generator import generate_report

# --- Model Configuration ---
class_names = {
    0: "Cassava Bacterial Blight (CBB)",
    1: "Cassava Brown Streak Disease (CBSD)",
    2: "Cassava Green Mottle (CGM)",
    3: "Cassava Mosaic Disease (CMD)",
    4: "Healthy"
}

class CropDiseaseModel:
    def __init__(self):
        self.model = None
        self.transform = None
        self.initialize_model()
        self.initialize_gemini()
        
    def initialize_model(self):
        """Initialize the PyTorch model"""
        # Initialize model (must match training setup)
        self.model = timm.create_model("rexnet_150", 
                                     pretrained=False, 
                                     num_classes=len(class_names))
        
        # Locate model file
        model_file = self._find_model_file()
        
        try:
            checkpoint = torch.load(model_file, map_location=torch.device('cpu'))
            # Clean state dict (remove DataParallel prefixes)
            state_dict = {k.replace("module.", ""): v for k, v in checkpoint.items()}
            self.model.load_state_dict(state_dict)
            self.model.eval()
            print(f"Model loaded successfully from {model_file}")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")
            
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225])
        ])
    
    def _find_model_file(self):
        """Search for the model file in multiple possible locations"""
        # First, check the path from environment variable
        if os.path.exists(MODEL_PATH):
            return MODEL_PATH
            
        # Try various relative paths
        base_dir = Path(__file__).parent.parent
        possible_paths = [
            base_dir / MODEL_PATH,
            base_dir / "models" / "crop_best_model.pth",
            base_dir.parent / "models" / "crop_best_model.pth",
            base_dir / "crop_best_model.pth"
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Create informative error message        
        print(f"ERROR: Model file not found. Searched in these locations:")
        print(f"- {MODEL_PATH}")
        for path in possible_paths:
            print(f"- {path}")
        print("Please place the model file in one of these locations or update MODEL_PATH in .env")
                
        raise FileNotFoundError("Could not find model file. Please check MODEL_PATH setting.")
    
    def initialize_gemini(self):
        """Initialize Google Gemini API connection"""
        if not GEMINI_API_KEY:
            print("Warning: No Gemini API key provided. Recommendations will use fallback mechanism.")
            self.gemini_model = None
            return
        
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
            # Test the API key with a simple prompt
            test_response = self.gemini_model.generate_content("Hello")
            print("Gemini API initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize Gemini API: {str(e)}")
            print("Recommendations will use fallback mechanism")
            self.gemini_model = None
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        # Convert to RGB (strip alpha channel if present)
        return image.convert("RGB")
        
    def predict(self, image):
        """Predict disease from image"""
        try:
            # Step 1: Convert to RGB
            rgb_image = self.preprocess_image(image)
            
            # Step 2: Apply transforms
            img_tensor = self.transform(rgb_image).unsqueeze(0)
            
            # Apply model prediction
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = F.softmax(outputs, dim=1)
            
            confidence, pred_idx = torch.max(probabilities, 1)
            return class_names[pred_idx.item()], confidence.item() * 100
            
        except Exception as e:
            raise RuntimeError(f"Prediction failed: {str(e)}")
    
    def get_recommendation(self, disease_name):
        """Get treatment recommendations from Gemini AI"""
        if not self.gemini_model:
            # Fallback recommendations for when Gemini API is not available
            if disease_name == "Healthy":
                return """- Maintain proper watering schedule (not too wet or dry)
- Apply balanced NPK fertilizer as recommended for cassava
- Keep the area around plants free of weeds
- Inspect plants weekly for early signs of pests or disease
- Ensure proper spacing between plants for good air circulation

Monitor for:
- Yellow discoloration of leaves
- Unusual spots or lesions
- Presence of insects or mites"""
            else:
                return f"""For {disease_name}:
- Immediately remove and destroy severely affected plants
- Apply copper-based fungicide (2g/liter) for bacterial diseases or appropriate fungicide for fungal diseases
- Ensure proper field drainage
- Use clean, disease-free planting material for new plantings
- Maintain proper spacing between plants for good air circulation
- Consider crop rotation if disease is persistent"""
        
        # Use Gemini API for recommendations if available
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
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3  # Lower = more factual (0-1 scale)
                )
            )
            return response.text.replace("•", "-")  # Normalize bullets
        except Exception as e:
            print(f"Error generating advice with Gemini: {str(e)}")
            # Fall back to basic recommendations
            return self.get_recommendation(None)  # This will use the fallback mechanism
    
    def generate_full_report(self, image, disease, confidence, recommendation):
        """Generate a complete PDF report"""
        try:
            # Create a temporary file with a unique name
            temp_file = None
            
            # Make a copy of the recommendation - in case it changes after getting used
            recommendation_copy = recommendation
            
            try:
                # Create temp directory if it doesn't exist
                os.makedirs(TEMP_DIR, exist_ok=True)
                
                # Use a timestamp in the filename to ensure uniqueness
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{timestamp}.jpg", dir=TEMP_DIR) as tmp:
                    temp_file = tmp.name
                    # Save the image with high quality
                    image.save(temp_file, "JPEG", quality=95)
                    
                print(f"Saved image to temporary file: {temp_file}")
                print(f"Starting PDF generation process...")
                
                # Generate the PDF report
                pdf_base64 = generate_report(
                    temp_file,
                    disease,
                    confidence,
                    recommendation_copy
                )
                
                return pdf_base64
                
            except Exception as e:
                print(f"Error in report generation: {str(e)}")
                import traceback
                print(traceback.format_exc())
                raise RuntimeError(f"Failed to generate report: {str(e)}")
                
            finally:
                # Clean up the temporary file
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                        print(f"Cleaned up temporary file: {temp_file}")
                    except Exception as e:
                        print(f"Warning: Could not clean up temporary file {temp_file}: {str(e)}")
                        
        except Exception as e:
            print(f"Error in report generation process: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise RuntimeError(f"Report generation failed: {str(e)}")

# Create a singleton instance
model_instance = CropDiseaseModel() 