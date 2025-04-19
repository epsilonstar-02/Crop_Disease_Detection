# Crop Disease Detection System

A full-stack application that uses AI to identify crop diseases from images and provide treatment recommendations.

## Project Overview

This project is an AI-powered crop disease detection system that helps farmers identify diseases in their crops through image analysis. It provides disease diagnosis, confidence scores, treatment recommendations, and generates detailed PDF reports.

## Tech Stack

### Backend

- **Framework**: Flask (Python)
- **ML/AI**:
  - PyTorch with timm (Transfer Learning)
  - RexNet-150 architecture for image classification
  - Google Gemini API for treatment recommendations
- **PDF Generation**: reportlab and fpdf2
- **Utilities**: Python-dotenv, Python-dateutil

### Frontend

- **Framework**: Dash (Python-based web application framework)
- **UI Components**: Dash Bootstrap Components
- **Styling**: Custom CSS with Bootstrap theming

## Project Architecture

```
Crop_Disease_Detection/
├── backend/                   # Backend Flask API
│   ├── app/                   # Main application code
│   │   ├── __init__.py        # Flask app initialization
│   │   ├── model.py           # Disease classification model
│   │   └── routes.py          # API endpoints
│   ├── models/                # Trained model files storage
│   ├── utils/                 # Utility functions
│   └── requirements.txt       # Python dependencies for backend
├── frontend/                  # Dash web interface
│   ├── app.py                 # Dash application setup
│   ├── callbacks.py           # UI interactivity
│   ├── layouts.py             # UI components and layout
│   ├── utils.py               # Frontend utility functions
│   └── assets/                # Static assets (images, etc.)
├── .env                       # Environment variables (create from .env.example)
└── run.py                     # Main entry point to run both frontend and backend
```

## Core Features

1. **Image Upload & Analysis**: Upload crop images for disease detection
2. **Disease Classification**: Identify specific crop diseases using a deep learning model
3. **Treatment Recommendations**: Get AI-generated treatment advice using Google Gemini
4. **PDF Report Generation**: Generate and download detailed reports with findings
5. **User-friendly Interface**: Clean, intuitive dashboard with image preview

## Technical Details

### Disease Classification Model

- The system uses a RexNet-150 architecture (pre-trained model fine-tuned for crop disease detection)
- The model classifies into 5 categories:
  - Cassava Bacterial Blight (CBB)
  - Cassava Brown Streak Disease (CBSD)
  - Cassava Green Mottle (CGM)
  - Cassava Mosaic Disease (CMD)
  - Healthy

### API Endpoints

- `/predict`: Accepts image upload, returns disease classification, confidence, and recommendations
- `/health`: Health check endpoint to verify API and model status

## How to Run the Project

### Prerequisites

- Python 3.8+ installed
- Git (to clone the repository)
- PyTorch (for model inference)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Crop_Disease_Detection
   ```

2. **Set up environment variables**

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your specific configuration
   # - Set GEMINI_API_KEY if you want AI-generated recommendations
   # - Update MODEL_PATH if needed
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the trained model**

   - Place the trained model file (`crop_best_model.pth`) in the `backend/models/` directory
   - Ensure the path matches the MODEL_PATH in your .env file

5. **Run the application**

   ```bash
   # Run both frontend and backend
   python run.py

   # To run only backend
   python run.py --component backend

   # To run only frontend
   python run.py --component frontend
   ```

6. **Access the web interface**
   - Open your browser and navigate to: http://127.0.0.1:8050
   - The backend API will be running at: http://127.0.0.1:5000

## Development

### Backend Development

- The backend is implemented as a Flask API
- The disease detection model is loaded at startup
- API endpoints handle image processing, prediction, and recommendation generation

### Frontend Development

- Built with Dash, a Python framework for building web applications
- Uses responsive Bootstrap components for layout
- Custom CSS for enhanced visuals
- Callbacks handle user interactions and API communication

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The disease classification model was trained on a dataset of crop disease images
- Google Gemini API for generating treatment recommendations
