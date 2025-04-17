# report_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import base64

def generate_report(image_path, disease, confidence, recommendation):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-50, "Crop Disease Diagnosis Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height-80, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Image
    c.drawImage(image_path, 50, height-320, width=200, height=200)

    # Diagnosis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-370, "Diagnosis:")
    c.setFont("Helvetica", 12)
    c.drawString(50, height-400, f"Disease: {disease}")
    c.drawString(50, height-425, f"Confidence: {confidence:.1f}%")

    # Recommendations
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height-470, "Recommendations:")
    text = c.beginText(50, height-500)
    text.setFont("Helvetica", 12)
    for line in recommendation.split('\n'):
        text.textLine(line.strip())
    c.drawText(text)

    c.save()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')