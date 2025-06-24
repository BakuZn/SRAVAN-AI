import pytesseract
import cv2
import os
from gtts import gTTS
import tempfile
import platform
import uuid

# Audio playback setup
if platform.system() == "Windows":
    import playsound
else:
    import subprocess

def play_audio(file_path):
    if platform.system() == "Windows":
        playsound.playsound(file_path)
    else:
        try:
            subprocess.call(["afplay", file_path])  # macOS
        except:
            subprocess.call(["mpg123", file_path])  # Linux

# Image file path
image_path = 'prescription_sample.jpg'

# Output text file path
extracted_text_file = 'extracted_prescription.txt'

# Begin OCR process
if not os.path.exists(image_path):
    print(f"Image file does not exist: {image_path}")
else:
    image = cv2.imread(image_path)
    if image is None:
        print("Image not loaded correctly.")
    else:
        print("Image loaded successfully.")
        try:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            extracted_text = pytesseract.image_to_string(gray_image).strip()

            print("Extracted Text:\n")
            print(extracted_text)

            if extracted_text:
                # Save text to file
                with open(extracted_text_file, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)

                # Convert text to speech (English with Indian accent)
                tts = gTTS(text=extracted_text, lang='en', tld='co.in')
                temp_path = os.path.join(tempfile.gettempdir(), f"sravan_audio_{uuid.uuid4().hex}.mp3")
                tts.save(temp_path)

                play_audio(temp_path)

                try:
                    os.remove(temp_path)
                except Exception as e:
                    print(f"Warning: Could not delete temp file: {e}")
            else:
                print("No text extracted from image.")

        except Exception as e:
            print(f"Error during OCR or TTS: {e}")
