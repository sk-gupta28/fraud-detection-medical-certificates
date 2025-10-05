import pytesseract
from PIL import Image
import random

# If using Windows, set the tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def analyze_certificate(file_path):
    try:
        text = pytesseract.image_to_string(Image.open(file_path))
        # Fake detection logic: random score or based on simple keywords
        score = random.randint(50, 100)
        status = "Authentic" if score > 70 else "Fraud"
        return {
            "text": text,
            "score": score,
            "status": status
        }
    except Exception as e:
        return {
            "text": "",
            "score": 0,
            "status": "Error"
        }
