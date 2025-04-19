"""
Utility functions for the frontend application.
"""

import base64
import io
from PIL import Image
import requests
from datetime import datetime


def parse_image_content(content):
    """
    Parse the base64 image content.
    
    Args:
        content (str): Base64 encoded image content
        
    Returns:
        bytes: Decoded image data
    """
    content_type, content_string = content.split(',')
    return base64.b64decode(content_string)


def get_image_details(decoded_data):
    """
    Get details of an image from its decoded data.
    
    Args:
        decoded_data (bytes): Decoded image data
        
    Returns:
        tuple: (width, height, format, size_kb)
    """
    img = Image.open(io.BytesIO(decoded_data))
    width, height = img.size
    img_format = img.format
    img_size = len(decoded_data) / 1024  # KB
    
    return width, height, img_format, img_size


def api_predict(image_data, api_url="http://localhost:5000/predict"):
    """
    Send the image to the API for prediction.
    
    Args:
        image_data (bytes): Decoded image data
        api_url (str): URL of the prediction API
        
    Returns:
        dict: API response as dictionary
    """
    response = requests.post(
        api_url,
        files={"image": image_data}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}")


def get_current_timestamp():
    """
    Get a formatted timestamp for the current time.
    
    Returns:
        str: Formatted timestamp
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_treatment_points(recommendation):
    """
    Format treatment recommendations into a list of points.
    
    Args:
        recommendation (str): Treatment recommendation text
        
    Returns:
        list: List of treatment points
    """
    treatment_points = recommendation.split('. ')
    return [point for point in treatment_points if point.strip()]


def get_severity(disease):
    """
    Determine disease severity based on the disease type.
    
    Args:
        disease (str): The disease name
        
    Returns:
        str: Severity level (Low, Medium, High)
    """
    if disease == "Healthy":
        return "None"
        
    severity_map = {
        "Cassava Bacterial Blight (CBB)": "High",
        "Cassava Brown Streak Disease (CBSD)": "High",
        "Cassava Green Mottle (CGM)": "Low",
        "Cassava Mosaic Disease (CMD)": "Medium"
    }
    
    # Look up in map or default to Medium if unknown disease
    return severity_map.get(disease, "Medium")


def get_spread_risk(disease):
    """
    Determine disease spread risk based on the disease type.
    
    Args:
        disease (str): The disease name
        
    Returns:
        str: Spread risk level (Low, Medium, High)
    """
    if disease == "Healthy":
        return "None"
        
    spread_risk_map = {
        "Cassava Bacterial Blight (CBB)": "High",
        "Cassava Brown Streak Disease (CBSD)": "Medium",
        "Cassava Green Mottle (CGM)": "Low",
        "Cassava Mosaic Disease (CMD)": "High"
    }
    
    # Look up in map or default to Medium if unknown disease
    return spread_risk_map.get(disease, "Medium")


def get_treatment_cost(disease):
    """
    Determine treatment cost based on the disease type.
    
    Args:
        disease (str): The disease name
        
    Returns:
        str: Treatment cost level (Low, Medium, High)
    """
    if disease == "Healthy":
        return "None"
        
    treatment_cost_map = {
        "Cassava Bacterial Blight (CBB)": "Medium",
        "Cassava Brown Streak Disease (CBSD)": "High",
        "Cassava Green Mottle (CGM)": "Low",
        "Cassava Mosaic Disease (CMD)": "Medium"
    }
    
    # Look up in map or default to Medium if unknown disease
    return treatment_cost_map.get(disease, "Medium") 