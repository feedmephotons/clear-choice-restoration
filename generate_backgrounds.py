#!/usr/bin/env python3
"""Generate themed textured backgrounds for Clear Choice Restoration website."""

import requests
import json
import base64
import os

API_KEY = "AIzaSyA8AVfoNKfSyy9Nkpp9gOv_X1qdeSttUQE"
MODEL = "gemini-2.0-flash-exp"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def generate_image(prompt, filename, aspect_ratio="16:9"):
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
        print(f"Error for {filename}: {response.status_code}")
        print(response.text)
        return False

    result = response.json()

    for candidate in result.get('candidates', []):
        for part in candidate['content']['parts']:
            if 'inlineData' in part:
                image_data = base64.b64decode(part['inlineData']['data'])
                filepath = f"Images/Backgrounds/{filename}"
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                print(f"Generated: {filepath}")
                return True

    print(f"No image generated for {filename}")
    return False

# Background prompts - subtle textures suitable for website sections
backgrounds = [
    {
        "filename": "storm-clouds-dark.jpg",
        "prompt": "Dramatic dark storm clouds background, moody atmospheric sky with deep navy blue and gray tones, subtle texture, NO TEXT, NO WORDS, NO LETTERS, abstract weather pattern suitable for website CTA section background, cinematic wide format, dark and dramatic but not too busy, professional quality"
    },
    {
        "filename": "sky-blue-texture.jpg",
        "prompt": "Soft light blue abstract texture background, subtle geometric patterns with sky blue (#6BA3D4) color palette, clean and professional, NO TEXT, NO WORDS, suitable for website section background with low opacity overlay, seamless subtle pattern, modern corporate design"
    },
    {
        "filename": "roofing-pattern-subtle.jpg",
        "prompt": "Subtle abstract roofing shingle pattern background, dark charcoal gray tones, geometric diamond/hexagon pattern inspired by architectural roof shingles, NO TEXT, NO LOGOS, very subtle low-contrast texture suitable for website background, professional minimalist design"
    },
    {
        "filename": "navy-gradient-texture.jpg",
        "prompt": "Deep navy blue (#1B4B8F) abstract gradient background with subtle noise texture, professional corporate design, NO TEXT, NO WORDS, smooth gradient from dark navy to slightly lighter navy, suitable for website CTA section overlay, elegant and sophisticated"
    },
    {
        "filename": "cream-paper-texture.jpg",
        "prompt": "Subtle cream colored paper texture background, warm off-white with very faint geometric pattern, NO TEXT, clean and minimal, suitable for light website section backgrounds, professional quality, soft warm tones like aged paper"
    }
]

print("Generating background textures for Clear Choice Restoration...")
print("=" * 60)

for bg in backgrounds:
    print(f"\nGenerating: {bg['filename']}")
    generate_image(bg['prompt'], bg['filename'])

print("\n" + "=" * 60)
print("Background generation complete!")
