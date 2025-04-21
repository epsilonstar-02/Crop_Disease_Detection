from fpdf import FPDF
from datetime import datetime
import base64
import os
from PIL import Image
import logging
from typing import Optional, Tuple
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_inputs(image_path: str, disease: str, confidence: float, recommendation: str) -> Tuple[bool, str]:
    """
    Validate input parameters for report generation
    
    Args:
        image_path: Path to the image file
        disease: Detected disease name
        confidence: Confidence score (0-100)
        recommendation: Treatment recommendations
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(image_path):
        return False, f"Image file not found: {image_path}"
        
    if not disease or not isinstance(disease, str):
        return False, "Invalid disease name"
        
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 100:
        return False, "Confidence must be a number between 0 and 100"
        
    if not recommendation or not isinstance(recommendation, str):
        return False, "Invalid recommendation text"
        
    return True, ""

def process_image(image_path: str, max_size: int = 1000) -> Optional[Image.Image]:
    """
    Process and validate the input image
    
    Args:
        image_path: Path to the image file
        max_size: Maximum dimension for resizing
        
    Returns:
        Processed PIL Image or None if processing fails
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        width, height = img.size
        if width > max_size or height > max_size:
            ratio = min(max_size/width, max_size/height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        return img
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return None

def generate_report(image_path: str, disease: str, confidence: float, recommendation: str) -> str:
    """
    Generate a PDF report based on diagnosis results using fpdf2
    
    Args:
        image_path: Path to the image file
        disease: Detected disease name
        confidence: Confidence score (0-100)
        recommendation: Treatment recommendations
        
    Returns:
        Base64 encoded PDF data
    """
    is_valid, error_msg = validate_inputs(image_path, disease, confidence, recommendation)
    if not is_valid:
        logger.error(f"Invalid inputs: {error_msg}")
        raise ValueError(error_msg)
    
    img = process_image(image_path)
    if img is None:
        raise ValueError("Failed to process image")
    
    temp_img_path = None
    pdf_buffer = None
    try:
        unique_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        temp_img_path = os.path.join(os.path.dirname(image_path), f"temp_{unique_id}.jpg")
        img.save(temp_img_path, "JPEG", quality=95)
        
        print(f"Creating PDF report...")
        print(f"Image path: {image_path}")
        print(f"Temporary image path: {temp_img_path}")
        print(f"Disease: {disease}")
        print(f"Recommendation length: {len(recommendation)} chars")
        
        pdf = FPDF()
        pdf.add_page()
        
        
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, "Crop Disease Diagnosis Report", ln=True, align='C')
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)
        
        try:
            if not os.path.exists(temp_img_path):
                raise FileNotFoundError(f"Temporary image file not found: {temp_img_path}")
            
            img_width, img_height = img.size
            aspect = img_width / float(img_height)
            display_width = 150  # mm
            display_height = display_width / aspect
            
            pdf.image(temp_img_path, x=30, y=pdf.get_y(), w=display_width, h=display_height)
            pdf.ln(display_height + 10)
            
        except Exception as e:
            logger.error(f"Error adding image to report: {str(e)}")
            pdf.cell(0, 10, "Image not available", ln=True)
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Diagnosis:", ln=True)
        
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Disease: {disease}", ln=True)
        pdf.cell(0, 10, f"Confidence: {confidence:.1f}%", ln=True)
        pdf.ln(10)
        
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, "Recommendations:", ln=True)
        
        pdf.set_font('Arial', '', 12)
        
        if not recommendation:
            recommendation = "No specific recommendations available."
        
        clean_recommendation = recommendation.replace("\r", "\n").replace("\t", "    ")
        
        paragraphs = clean_recommendation.split('\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                # Multi-cell for text wrapping
                pdf.multi_cell(0, 10, paragraph.strip())
                pdf.ln(5)
        
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        pdf_data = pdf_buffer.getvalue()
        encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        if len(encoded_pdf) < 100:
            print(f"WARNING: Generated PDF is suspiciously small ({len(encoded_pdf)} bytes)")
        else:
            print(f"PDF generated successfully ({len(encoded_pdf)} bytes)")
            
        return encoded_pdf
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        raise RuntimeError(f"Failed to generate PDF report: {str(e)}")
        
    finally:
        if temp_img_path and os.path.exists(temp_img_path):
            try:
                os.unlink(temp_img_path)
                print(f"Deleted temporary image file: {temp_img_path}")
            except Exception as e:
                logger.warning(f"Error deleting temporary image: {str(e)}")
        
        if pdf_buffer:
            try:
                pdf_buffer.close()
            except Exception as e:
                logger.warning(f"Error closing PDF buffer: {str(e)}")
        
        if img:
            try:
                img.close()
            except Exception as e:
                logger.warning(f"Error closing image: {str(e)}")