from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import base64
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

api_key = "jsn"  # Replace with your actual OpenAI API key

@app.route('/upload-image', methods=['POST'])
def upload_image():
    file = request.files['file']
    base64_image = base64.b64encode(file.read()).decode('utf-8')

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Respond in HTML format: Calculate the total resistance and capacitance."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Debug: print the full response data to the console
    print("OpenAI API Response:", response_data)

    if 'choices' in response_data and len(response_data['choices']) > 0:
        extended_response = response_data['choices'][0].get('message', {}).get('content', 'No response found.')
    else:
        extended_response = 'No response found.'

    return jsonify({"gpt_response": extended_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
