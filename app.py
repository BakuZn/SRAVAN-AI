from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/voice_query', methods=['POST'])
def voice_query():
    query = request.form.get('query', '')
    # Process the query (you'll implement this)
    response = f"Processed your query: {query}"
    return jsonify({'message': response})

@app.route('/upload_prescription', methods=['POST'])
def upload_prescription():
    if 'file' not in request.files:
        return jsonify({'message': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Process the prescription using your OCR script
    try:
        subprocess.run(['python', 'ocr_tts.py', filepath], check=True)
        return jsonify({'message': 'Prescription processed successfully'})
    except subprocess.CalledProcessError:
        return jsonify({'message': 'Error processing prescription'}), 500

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    try:
        subprocess.run(['python', 'medicine_reminder.py'], check=True)
        return jsonify({'message': 'Reminders set successfully'})
    except subprocess.CalledProcessError:
        return jsonify({'message': 'Error setting reminders'}), 500

if __name__ == '__main__':
    app.run(debug=True)