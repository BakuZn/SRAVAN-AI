import speech_recognition as sr
from gtts import gTTS
import tempfile
import platform
import subprocess
import os
import uuid
import difflib

# Initialize recognizer
recognizer = sr.Recognizer()

# FAQ database with both Hindi and English keywords
faq = {
    # PM Kisan
    "pm kisan": "PM Kisan Yojana ek kendriya yojana hai jisme har registered kisan ko 6000 rupaye pratisaal teen kisto mein diye jaate hain.",
    "पीएम किसान": "पीएम किसान योजना में पंजीकृत किसानों को सालाना 6000 रुपये तीन किश्तों में मिलते हैं।",
    "pm kisan kya hai": "PM Kisan Yojana mein kisanon ko har saal 6000 rupaye diye jaate hain.",
    "पीएम किसान क्या है": "यह योजना किसानों को 6000 रुपये सालाना तीन किश्तों में देती है।",

    # Ayushman Bharat
    "ayushman bharat": "Ayushman Bharat ek health insurance scheme hai jisme gareeb parivaron ko 5 lakh rupaye tak ka muft ilaj milta hai.",
    "आयुष्मान भारत": "आयुष्मान भारत योजना में गरीबों को 5 लाख रुपये तक का मुफ्त इलाज मिलता है।",
    "ayushman card": "Ayushman card se aap kisi bhi listed hospital mein bina paisa diye ilaj kara sakte hain.",
    "आयुष्मान कार्ड": "आयुष्मान कार्ड से आप सरकारी और चुने गए प्राइवेट अस्पतालों में मुफ्त इलाज करा सकते हैं।",

    # Ration Card
    "ration card": "Ration card ek dastavej hai jisse aap sarkari sasta anaaj prapt kar sakte hain.",
    "राशन कार्ड": "राशन कार्ड से आपको सरकारी दर पर अनाज मिलता है।",
    "ration lene ka card": "Ration lene ke liye sarkar dwara diya gaya card hota hai.",
    "सस्ता राशन कार्ड": "राशन कार्ड से आप सस्ता राशन ले सकते हैं।",

    # Pension
    "pension": "Sarkari pension yojana mein vridh, vidhwa, aur viklang nagrikon ko pratyek mahine kuch dhanrashi di jaati hai.",
    "पेंशन": "सरकारी योजना के तहत वृद्धों को हर महीने पेंशन दी जाती है।",
    "pension kaise milegi": "Aap nagar nigam ya panchayat mein avedan karke pension prapt kar sakte hain.",
    "पेंशन कैसे मिलती है": "आप अपने निकटतम कार्यालय में आवेदन कर सकते हैं।",

    # Aadhaar
    "aadhar": "Aadhaar card ek 12 ank ka number hai jo vyakti ki pehchaan batata hai.",
    "aadhar card": "Aadhaar card ka upyog kai sarkari suvidhao mein hota hai.",
    "आधार": "आधार कार्ड पहचान का सबसे जरूरी दस्तावेज है।",
    "आधार कार्ड": "यह सरकारी योजनाओं में पहचान के लिए आवश्यक है।",
    "aadhar card banana hai": "Aapko Aadhaar center jaakar form bharna hoga.",

    # Bank Account
    "bank account": "Bank account ek aarthik suvidha hai jisme paisa jama aur nikaal sakte hain.",
    "बैंक खाता": "बैंक खाता सरकारी योजनाओं का लाभ पाने के लिए जरूरी होता है।",
    "zero balance account": "Jan Dhan ke tahat zero balance account khulta hai.",
    "जनधन खाता": "जनधन योजना mein bina minimum balance ke account khulta hai.",

    # Insurance / Bima
    "insurance": "Insurance ek suraksha yojana hai jo aapko haadse ke samay arthik madad deti hai.",
    "insurance kya hota hai": "Yeh ek financial suraksha hai jo aapke aur aapke parivar ko protection deti hai.",
    "इंश्योरेंस": "बीमा ek suraksha yojana hai jo accident ke samay paisa deti hai.",
    "बीमा": "बीमा से मृत्यु या दुर्घटना के समय आर्थिक मदद मिलती है।",
    "pradhan mantri bima": "PM Suraksha Bima mein sirf 12 rupaye mein 2 lakh ka accident cover milta hai.",
    "प्रधानमंत्री बीमा": "12 रुपये वार्षिक पर दुर्घटना बीमा मिलता है।",

    # Government Help
    "government help": "Sarkar kai yojnaayein chalati hai jaise PM Kisan, Ayushman Bharat, Ration Card, Pension, Bank account.",
    "सरकारी सहायता": "सरकार गरीबों, वृद्धों और किसानों के लिए kai yojnaayein chalati hai.",
    "madad chahiye": "Bataiye kis vishay mein madad chahiye — ilaj, ration ya paisa.",
    "मदद चाहिए": "आपको इलाज, राशन या पैसे की जरूरत है क्या?",
    "madad chahie": "Kis vishay mein madad chahiye? Ration, pension ya aayushman?"
}


# Audio playback
def play_audio(file_path):
    if platform.system() == "Windows":
        import playsound
        playsound.playsound(file_path)
    else:
        try:
            subprocess.call(["afplay", file_path])
        except:
            subprocess.call(["mpg123", file_path])

# Speak text using gTTS
def speak(text):
    print("Response:", text)
    try:
        tts = gTTS(text=text, lang='hi')
        temp_path = os.path.join(tempfile.gettempdir(), f"sravan_{uuid.uuid4().hex}.mp3")
        tts.save(temp_path)
        play_audio(temp_path)
        os.remove(temp_path)
    except Exception as e:
        print("TTS Error:", e)

# Match user query to best available FAQ keyword
def find_best_match(query):
    query = query.lower()
    matches = difflib.get_close_matches(query, faq.keys(), n=1, cutoff=0.4)
    if matches:
        return matches[0]
    
    # Also check if any keyword is part of user query
    for keyword in faq:
        if keyword in query:
            return keyword
    return None

# Listen and respond
def listen_and_answer():
    with sr.Microphone() as source:
        print("Boliye, aap kya jaanna chahte hain...")
        audio = recognizer.listen(source)

        try:
            # First try Hindi
            try:
                query = recognizer.recognize_google(audio, language='hi-IN').lower()
            except sr.UnknownValueError:
                # Fallback to English
                query = recognizer.recognize_google(audio, language='en-IN').lower()

            print("Aapne poocha:", query)
            best_match = find_best_match(query)

            if best_match:
                speak(faq[best_match])
            else:
                speak("Maaf kijiye, main is prashna ka uttar nahi de sakta.")

        except sr.UnknownValueError:
            speak("Maaf kijiye, aapki awaaz samajh nahi aayi.")
        except sr.RequestError:
            speak("Speech service uplabdh nahi hai. Kripya internet connection janchiye.")

# Run the voice assistant once
if __name__ == "__main__":
    listen_and_answer()
