from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import pytesseract
from PIL import Image
from io import BytesIO
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values 

# Instantiate the app
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
openai = OpenAI() 


load_dotenv() 

# Route for uploading image
@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'image' in request.files:
            # Handle image uploaded from file
            image_file = request.files['image']
            image = Image.open(image_file)
        elif 'imageDataURL' in request.json:
            # Handle image data URL (e.g., captured from camera)
            imageDataURL = request.json['imageDataURL']
            image_data = base64.b64decode(imageDataURL.split(',')[1])
            image = Image.open(BytesIO(image_data))
        else:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Perform OCR using Tesseract
        extracted_text = pytesseract.image_to_string(image)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "summarize this product label in different points (numbered). and add extra information when needed"},
                {"role": "user", "content": extracted_text}
            ]
        )
        summary =  response.choices[0].message.content
        return jsonify({'text': extracted_text, 'summary': summary})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
