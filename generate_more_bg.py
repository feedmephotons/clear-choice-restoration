#!/usr/bin/env python3
"""Generate additional background textures."""

import requests
import json
import base64
import os

API_KEY = "AIzaSyA8AVfoNKfSyy9Nkpp9gOv_X1qdeSttUQE"
MODEL = "gemini-2.0-flash-exp"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def generate_image(prompt, filename):
    """Generate an image using Gemini API."""
    request_body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    response = requests.post(
        f"{BASE_URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_body)
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return False

    result = response.json()
    for candidate in result.get('candidates', []):
        content = candidate.get('content', {})
        for part in content.get('parts', []):
            if 'inlineData' in part:
                image_data = base64.b64decode(part['inlineData']['data'])
                filepath = f"Images/Backgrounds/{filename}"
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                print(f"Generated: {filepath}")
                return True
    return False

# Generate remaining backgrounds
backgrounds = [
    {
        "filename": "navy-abstract.jpg",
        "prompt": "Abstract deep navy blue background texture with subtle gradient and soft noise, corporate professional design, smooth dark blue (#1B4B8F) tones, suitable for website overlay background, no text, no logos, elegant minimal design"
    },
    {
        "filename": "warm-cream-subtle.jpg",
        "prompt": "Warm cream colored subtle texture background, soft off-white with gentle paper-like texture, very light and clean, no text, minimal design suitable for website content sections, professional quality"
    }
]

for bg in backgrounds:
    print(f"Generating: {bg['filename']}")
    generate_image(bg['prompt'], bg['filename'])

print("Done!")
