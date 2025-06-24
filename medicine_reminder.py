import time
import re
from gtts import gTTS
import os
import platform
import uuid
import tempfile
from datetime import datetime
from plyer import notification  # pip install plyer

# Audio playback setup
if platform.system() == "Windows":
    import playsound
else:
    import subprocess

def play_audio(text):
    print(f"🔊 Announcing: {text}")
    tts = gTTS(text=text, lang='en', tld='co.in')  # Indian English
    temp_path = os.path.join(tempfile.gettempdir(), f"remind_{uuid.uuid4().hex}.mp3")
    tts.save(temp_path)
    if platform.system() == "Windows":
        playsound.playsound(temp_path)
    else:
        try:
            subprocess.call(["afplay", temp_path])
        except:
            subprocess.call(["mpg123", temp_path])
    try:
        os.remove(temp_path)
    except:
        pass

def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='SRAVAN Reminder',
        timeout=10
    )

# Load extracted OCR text
file_path = 'extracted_prescription.txt'
if not os.path.exists(file_path):
    print("❌ Prescription file not found.")
    exit()

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract medicine reminders
lines = text.splitlines()
reminders = []
pattern = re.compile(r"(TAB\.|CAP\.|TABLET|CAPSULE)?\s*([A-Za-z0-9\-]+)\s+.*?(morning|night|evening)", re.IGNORECASE)

for line in lines:
    match = pattern.search(line)
    if match:
        med = match.group(2).strip()
        time_of_day = match.group(3).lower()
        if time_of_day in ['morning', 'evening', 'night']:
            reminders.append((med, time_of_day))

reminders = list(set(reminders))  # Deduplicate

schedule = {
    'morning': 8,
    'evening': 17,
    'night': 21
}

if not reminders:
    print("⚠️ No valid medicine reminders found.")
    exit()

print("🕐 Scheduled Reminders:")
for med, time_of_day in reminders:
    print(f" - {med} at {time_of_day.title()}")

# Detect Follow-up date
followup_date = None
followup_notified = False  # To avoid repeated alerts

date_match = re.search(r"follow[\s\-]?up[\s:]*([\d\/\-]+)", text, re.IGNORECASE)
if date_match:
    raw_date = date_match.group(1).strip()
    for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y"):
        try:
            parsed_date = datetime.strptime(raw_date, fmt).date()
            followup_date = parsed_date
            print(f"📅 Follow-up Date Found: {followup_date}")
            break
        except ValueError:
            continue
else:
    print("⚠️ No follow-up date found.")

print("\n✅ Reminder system is now running...\n")

# Main loop
try:
    while True:
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        # Medicine Reminders
        for med, timing in reminders:
            if hour == schedule[timing] and minute == 0:
                message = f"Time to take your medicine: {med}"
                send_notification("Medicine Reminder", message)
                play_audio(message)
                time.sleep(60)

        # Follow-up Reminder at 10:00 AM
        if followup_date and not followup_notified:
            today = datetime.today().date()
            if today == followup_date and hour == 10 and minute == 0:
                message = "Today is your follow-up day. Please visit your doctor."
                send_notification("Follow-Up Reminder", message)
                play_audio(message)
                followup_notified = True
                time.sleep(60)

        time.sleep(20)

except KeyboardInterrupt:
    print("🔴 Reminder system stopped.")
