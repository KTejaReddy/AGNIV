import easyocr
import numpy as np
from PIL import Image
from app.core.logging import logger
from .session import screen_session

class OCREngine:
    def __init__(self):
        self.reader = None
        self.is_loaded = False

    def _load(self):
        if not self.is_loaded:
            logger.info("Loading EasyOCR Model...")
            # We initialize standard English by default. 
            # In production, this would read from user configuration.
            self.reader = easyocr.Reader(['en'], gpu=False) # CPU for broad compatibility initially
            self.is_loaded = True
            logger.info("EasyOCR Model Loaded")

    def run_ocr_on_image(self, image_data):
        """
        Runs OCR on a numpy array (BGR or RGB) or PIL Image.
        """
        try:
            self._load()
            
            # Convert to numpy if needed
            if isinstance(image_data, Image.Image):
                image_data = np.array(image_data)
                
            results = self.reader.readtext(image_data)
            
            parsed_results = []
            for (bbox, text, prob) in results:
                parsed_results.append({
                    "text": text,
                    "confidence": float(prob),
                    "box": [
                        [int(bbox[0][0]), int(bbox[0][1])], # top left
                        [int(bbox[2][0]), int(bbox[2][1])]  # bottom right
                    ]
                })
                
            screen_session.update_state("ocr_results", parsed_results)
            return parsed_results
            
        except Exception as e:
            logger.error(f"OCR Error: {e}")
            return []

ocr_engine = OCREngine()
