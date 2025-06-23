from gtts import gTTS
import os

text = "Testing voice. Hello Daksh!"
tts = gTTS(text=text, lang='en', tld='co.in')  # Indian accent

tts.save("test_audio.mp3")
print("✅ Audio saved as test_audio.mp3")

os.system("start test_audio.mp3")
