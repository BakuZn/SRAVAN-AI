import pytesseract
import cv2
import pyttsx3
from PIL import Image
import os

image_path = 'prescription_sample.jpg'

if not os.path.exists(image_path):
    print(f"❌ Image file does not exist: {image_path}")
else:
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Image not found or not loaded correctly.")
    else:
        print("✅ Image loaded successfully.")
        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray_image)
            print("Extracted Text:")
            print(extracted_text)
            engine = pyttsx3.init()
            engine = pyttsx3.init()
            engine.say(extracted_text)
            engine.runAndWait()
            engine.say(extracted_text)
            engine.runAndWait()
        except Exception as e:
            print(f"❌ Error during text extraction or speech synthesis: {e}")
