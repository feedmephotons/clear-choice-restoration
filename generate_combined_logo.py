#!/usr/bin/env python3
"""
Generate combined logo for Clear Choice Restoration
Uses both logo symbol and logo text as reference images
"""

import requests
import json
import base64
from pathlib import Path

# API Configuration
API_KEY = "AIzaSyA8AVfoNKfSyy9Nkpp9gOv_X1qdeSttUQE"
MODEL = "gemini-3-pro-image-preview"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# Paths
BASE_DIR = Path("/home/wfowlkes/Claude Main Projects/Clear Choice Restoration")
LOGO_SYMBOL_PATH = BASE_DIR / "Images/Logos/CCR_House_Hands_2C (1).jpg"
OUTPUT_DIR = BASE_DIR / "Images/Logos"

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_combined_logo():
    """Generate combined logo with symbol and text"""

    prompt = """Create a professional combined company logo for Clear Choice Restoration.

    I am providing the logo symbol (a house cradled in two hands in blue tones).

    Create a complete horizontal logo layout with:

    LEFT SIDE: The house-in-hands symbol from the reference image - keep it exactly as shown
    with the same two-tone blue colors (dark navy #1B4B8F for the hands and window,
    light sky blue #6BA3D4 for the roof outline).

    RIGHT SIDE: The company name text "CLEAR CHOICE" on top in bold italic style
    matching the original logo font, and "RESTORATION" below it in a clean sans-serif,
    all in the dark navy blue color (#1B4B8F). The word RESTORATION should have
    decorative bars on either side.

    Layout: Symbol on left, text on right, properly balanced and proportioned.
    Background: Pure white/transparent suitable for website header use.

    Style: Clean, professional logo suitable for a roofing/restoration company.
    Maintain exact colors from the reference.

    NO watermarks, NO extra decorations."""

    parts = [
        {"text": prompt},
        {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": encode_image(LOGO_SYMBOL_PATH)
            }
        }
    ]

    # Generate horizontal version
    print("Generating combined logo (horizontal)...")

    request_body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": "21:9",
                "imageSize": "2K"
            }
        }
    }

    response = requests.post(
        f"{BASE_URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_body),
        timeout=120
    )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text[:500]}")
        return

    result = response.json()

    for candidate in result.get('candidates', []):
        for part in candidate.get('content', {}).get('parts', []):
            if 'inlineData' in part:
                image_data = base64.b64decode(part['inlineData']['data'])
                output_path = OUTPUT_DIR / "CCR_Combined_Logo_Horizontal.png"
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                print(f"  Saved: {output_path}")
                break

    # Generate square/stacked version for favicon/mobile
    print("\nGenerating combined logo (stacked)...")

    stacked_prompt = """Create a stacked/square version of this company logo.

    Using the house-in-hands symbol from the reference image:

    TOP: The house-in-hands symbol centered, keeping exact colors
    (dark navy #1B4B8F for hands/window, light sky blue #6BA3D4 for roof)

    BOTTOM: Text "CLEAR CHOICE" in bold italic, "RESTORATION" below it,
    both centered, in dark navy blue (#1B4B8F)

    Background: Pure white
    Layout: Compact, balanced, suitable for square format

    NO watermarks."""

    parts_stacked = [
        {"text": stacked_prompt},
        {
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": encode_image(LOGO_SYMBOL_PATH)
            }
        }
    ]

    request_body_stacked = {
        "contents": [{"parts": parts_stacked}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": "1:1",
                "imageSize": "2K"
            }
        }
    }

    response_stacked = requests.post(
        f"{BASE_URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_body_stacked),
        timeout=120
    )

    if response_stacked.status_code == 200:
        result_stacked = response_stacked.json()
        for candidate in result_stacked.get('candidates', []):
            for part in candidate.get('content', {}).get('parts', []):
                if 'inlineData' in part:
                    image_data = base64.b64decode(part['inlineData']['data'])
                    output_path = OUTPUT_DIR / "CCR_Combined_Logo_Stacked.png"
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    print(f"  Saved: {output_path}")
                    break

if __name__ == "__main__":
    generate_combined_logo()
