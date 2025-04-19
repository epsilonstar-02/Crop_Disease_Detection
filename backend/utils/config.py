import os
from dotenv import load_dotenv
import pathlib
import tempfile

# Load environment variables from .env file
base_dir = pathlib.Path(__file__).parent.parent.parent
load_dotenv(os.path.join(base_dir, ".env"))

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

# AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model Configuration
MODEL_PATH = os.getenv("MODEL_PATH", "models/crop_best_model.pth")

# Temporary files configuration
# Use system temp directory with a project-specific subdirectory
TEMP_DIR = os.path.join(tempfile.gettempdir(), "crop_disease_detection")
os.makedirs(TEMP_DIR, exist_ok=True) 