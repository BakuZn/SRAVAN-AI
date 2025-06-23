import pytesseract
import cv2
import os
from gtts import gTTS
import tempfile
import platform
import uuid

# For audio playback
if platform.system() == "Windows":
    import playsound
else:
    import subprocess

# Function to play audio
def play_audio(file_path):
    if platform.system() == "Windows":
        playsound.playsound(file_path)
    else:
        try:
            subprocess.call(["afplay", file_path])  # macOS
        except:
            subprocess.call(["mpg123", file_path])  # Linux

# Image path
image_path = 'prescription_sample.jpg'

# Process the image
if not os.path.exists(image_path):
    print(f"Image file does not exist: {image_path}")
else:
    image = cv2.imread(image_path)
    if image is None:
        print("Image not loaded correctly.")
    else:
        print("Image loaded successfully.")
        try:
            # Convert to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # OCR text extraction
            extracted_text = pytesseract.image_to_string(gray_image)
            text = extracted_text.strip()
            print("Extracted Text:\n")
            print(text)

            if text:
                # Save TTS audio to unique temp file
                tts = gTTS(text=text, lang='hi')  # Use Hindi TTS (understandable for both Hindi + English)
                temp_path = os.path.join(tempfile.gettempdir(), f"sravan_audio_{uuid.uuid4().hex}.mp3")
                tts.save(temp_path)

                # Play and remove file
                play_audio(temp_path)
                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Warning: Could not delete temp file: {e}")
            else:
                print("No text extracted from image.")
        except Exception as e:
            print(f"Error during text extraction or speech synthesis: {e}")
