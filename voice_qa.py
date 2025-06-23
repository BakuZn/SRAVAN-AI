import speech_recognition as sr
import pyttsx3

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speaking speed

# Basic Q&A data
faq = {
    "pm kisan": "PM Kisan Yojana ek sarkari yojana hai jo kisano ko 6000 rupaye prati varsh deti hai.",
    "ration card": "Ration card ek government document hai jo aapko subsidised anaaj prapt karne mein madad karta hai.",
    "ayushman bharat": "Ayushman Bharat ek health scheme hai jisme 5 lakh tak ka free ilaj diya jaata hai.",
    "pension": "Vridhavastha pension yojana mein buzurgon ko pratyek mahine sarkar dwara kuch dhanrashi di jaati hai."
}

# Text-to-speech output
def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()

# Voice input + response
def listen_and_answer():
    with sr.Microphone() as source:
        print("🟢 Boliye, aap kya jaanna chahte hain...")
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio, language='hi-IN').lower()
            print(f"🔍 Aapne poocha: {query}")

            # Match question to known answers
            for keyword in faq:
                if keyword in query:
                    speak(faq[keyword])
                    break
            else:
                speak("Maaf kijiye, main is prashna ka uttar nahi de sakta.")

        except sr.UnknownValueError:
            speak("Maaf kijiye, aapki awaaz samajh nahi aayi.")
        except sr.RequestError:
            speak("Speech service uplabdh nahi hai. Kripya internet connection janchiye.")

# Run Q&A once for demo
listen_and_answer()
