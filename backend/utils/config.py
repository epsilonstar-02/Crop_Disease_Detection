import os
from dotenv import load_dotenv
import pathlib
import tempfile

base_dir = pathlib.Path(__file__).parent.parent.parent
load_dotenv(os.path.join(base_dir, ".env"))

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

MODEL_PATH = os.getenv("MODEL_PATH", "models/crop_best_model.pth")

TEMP_DIR = os.path.join(tempfile.gettempdir(), "crop_disease_detection")
os.makedirs(TEMP_DIR, exist_ok=True) 