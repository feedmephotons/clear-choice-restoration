#!/usr/bin/env python3
"""
Image generator for Clear Choice Restoration website
Uses Gemini gemini-3-pro-image-preview model for high-quality image generation
"""

import requests
import json
import base64
import os
from pathlib import Path

# API Configuration
API_KEY = "AIzaSyA8AVfoNKfSyy9Nkpp9gOv_X1qdeSttUQE"
MODEL = "gemini-3-pro-image-preview"
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# Paths
BASE_DIR = Path("/home/wfowlkes/Claude Main Projects/Clear Choice Restoration")
LOGO_SYMBOL_PATH = BASE_DIR / "Images/Logos/CCR_House_Hands_2C (1).jpg"
OUTPUT_DIR = BASE_DIR / "Images/Site"

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def generate_image(prompt, reference_images=None, aspect_ratio="16:9", image_size="2K", filename=None):
    """
    Generate an image using Gemini gemini-3-pro-image-preview model
    """
    parts = [{"text": prompt}]

    # Add reference images if provided
    if reference_images:
        for img_path in reference_images:
            if os.path.exists(img_path):
                encoded = encode_image(img_path)
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": encoded
                    }
                })

    request_body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size
            }
        }
    }

    print(f"Generating: {filename or 'image'}...")

    response = requests.post(
        f"{BASE_URL}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(request_body),
        timeout=120
    )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text[:500]}")
        return None

    result = response.json()
    images = []

    for candidate in result.get('candidates', []):
        for part in candidate.get('content', {}).get('parts', []):
            if 'inlineData' in part:
                images.append(base64.b64decode(part['inlineData']['data']))

    if images and filename:
        output_path = OUTPUT_DIR / filename
        with open(output_path, 'wb') as f:
            f.write(images[0])
        print(f"  Saved: {output_path}")

    return images

def main():
    """Generate all site images"""

    logo_path = str(LOGO_SYMBOL_PATH)

    # Image generation prompts
    images_to_generate = [
        {
            "filename": "hero-banner.jpg",
            "aspect_ratio": "21:9",
            "prompt": """Create a professional hero banner image for a roofing company website:

            Scene: A beautiful residential home in Indianapolis, Indiana suburbs on a clear day.
            The home has a pristine new asphalt shingle roof in charcoal gray color.
            The Indianapolis skyline is subtly visible in the distant background.

            Style: Clean, professional commercial photography. Warm natural lighting suggesting
            morning golden hour. Slight low angle looking up at the home to emphasize the roof.

            Colors: Rich blues in the sky that complement the brand colors (dark navy blue #1B4B8F
            and light sky blue #6BA3D4). Green lawn, traditional Midwestern architecture.

            NO text, NO watermarks, NO people in this image."""
        },
        {
            "filename": "hail-damage-inspection.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional photograph showing a roofing contractor inspecting
            hail damage on a residential roof in Indianapolis:

            Scene: A professional male roofing inspector on a residential asphalt shingle roof,
            crouching down and examining hail damage marks on shingles. He's pointing at visible
            dents and damage spots on the shingles. He is wearing a dark navy blue polo shirt
            (color #1B4B8F) with a small logo emblem on the chest - the logo is a simple house
            shape cradled by two hands in light blue (#6BA3D4).

            The inspector is wearing a hard hat for safety. There are visible circular dent
            marks on the shingles from hail impact - the damage is clearly visible.

            Setting: Midwestern residential neighborhood, overcast sky typical after a storm.

            Style: Documentary-style commercial photography, natural lighting, professional
            but approachable. The image should convey expertise and trustworthiness.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "roofing-team.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional team photograph for a roofing company:

            Scene: Three professional roofing contractors standing confidently in front of a
            completed residential roofing job in Indianapolis. The home behind them has a
            beautiful new roof installation.

            The team consists of three diverse professionals - a mix of ages and appearances
            to represent a family-owned business feel. They are all wearing matching dark navy
            blue polo shirts (color #1B4B8F) with a company logo on the left chest. The logo
            emblem shows a simple house shape being held by two cupped hands in a lighter
            blue color (#6BA3D4).

            One person holds a clipboard, another has arms crossed confidently. They are
            all smiling warmly and looking professional.

            Style: Professional commercial photography, natural daylight, friendly and
            approachable team portrait. Conveys trustworthiness and family-owned values.

            NO text overlays, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "new-roof-installation.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional photograph of active roof installation work:

            Scene: Two roofing workers actively installing new asphalt shingles on a
            residential home roof in Indianapolis. One worker is using a nail gun on
            shingles while the other is positioning the next row.

            Both workers are wearing dark navy blue work shirts (color #1B4B8F) with
            a small logo on the back - a house shape held by two hands in light blue.
            They are wearing proper safety equipment including hard hats.

            The roof is partially complete, showing the transition from old/bare
            decking to new underlayment to finished shingles - demonstrating the
            installation process.

            Setting: Clear sunny day in a Midwestern residential neighborhood.
            Traditional Indianapolis-style homes visible in background.

            Style: Action shot, documentary commercial photography. Shows skilled
            craftsmanship and professionalism.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "storm-damage-roof.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a realistic photograph showing storm and hail damage
            to a residential roof that needs repair:

            Scene: Close-up view of a damaged asphalt shingle roof on an Indianapolis
            home after a severe hailstorm. The damage is clearly visible:
            - Multiple circular dent marks from hail impacts
            - Some cracked and broken shingles
            - Missing granules on shingle surfaces
            - A few lifted or displaced shingles

            The damage should look realistic but not completely destroyed - repairable
            by professionals.

            Setting: Overcast sky suggesting recent storm. Residential Midwestern
            neighborhood context.

            Style: Documentary photography, realistic damage documentation photo like
            what would be taken for an insurance claim. Sharp focus on the damage.

            NO people, NO text, NO watermarks."""
        },
        {
            "filename": "gutter-installation.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional photograph of gutter installation service:

            Scene: A professional contractor installing new aluminum gutters on a
            residential home in Indianapolis. He is on a ladder, attaching a new
            white seamless gutter to the fascia board.

            The worker is wearing a dark navy blue polo shirt (color #1B4B8F) with
            a small company logo emblem on the chest - a house shape cradled by
            hands in light blue (#6BA3D4).

            Tools and materials are organized professionally. The home is a typical
            Midwestern residential property.

            Style: Professional commercial photography, natural lighting, shows
            skilled craftsmanship and attention to detail.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "free-inspection.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional photograph showing a roofing company
            representative meeting with a homeowner for a free roof inspection:

            Scene: A friendly professional roofing consultant in a dark navy blue
            polo shirt (color #1B4B8F) with a small house-and-hands logo emblem,
            standing at the front door of a nice Indianapolis suburban home,
            greeting a homeowner couple.

            The consultant has a clipboard and is pointing up toward the roof,
            explaining something to the attentive homeowners. Everyone looks
            friendly and professional - this represents the start of a free
            inspection consultation.

            Setting: Front yard/porch of a typical Midwestern residential home
            on a pleasant day.

            Style: Warm, approachable commercial photography. Conveys trust,
            professionalism, and customer service.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "siding-work.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a professional photograph of vinyl siding installation:

            Scene: A contractor installing new vinyl siding on a residential home
            in Indianapolis. He is using proper tools to secure a panel of neutral-
            colored vinyl siding to the exterior wall.

            The worker wears a dark navy blue work shirt (color #1B4B8F) with a
            company logo on the back - a house shape held by cupped hands in
            light blue (#6BA3D4).

            Part of the wall shows the completed siding while another section
            shows the work in progress with house wrap visible.

            Setting: Sunny day, residential Midwestern neighborhood.

            Style: Professional commercial photography showing skilled installation
            work. Clean and professional atmosphere.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "about-family-business.jpg",
            "aspect_ratio": "3:2",
            "prompt": """Create a warm, professional photograph representing a
            family-owned roofing business:

            Scene: An office/meeting room setting where a small team of 3-4 people
            representing a family-owned business are gathered around a table looking
            at roofing material samples and plans together.

            The people should look like they could be family members or long-time
            colleagues - warm and collaborative atmosphere. Mix of ages showing
            experience passed down.

            On the wall behind them is the company logo - a house shape cradled
            by two hands in blue tones. They are wearing professional casual
            attire in navy blue tones.

            Style: Warm, inviting commercial photography. Conveys family values,
            trust, and decades of experience. Natural indoor lighting.

            NO text overlays, NO watermarks.""",
            "reference_images": [logo_path]
        },
        {
            "filename": "emergency-service.jpg",
            "aspect_ratio": "16:9",
            "prompt": """Create a dramatic photograph representing 24-hour emergency
            roofing service:

            Scene: A roofing service truck/van parked in front of a residential home
            during dusk/twilight hours. The sky shows dramatic post-storm clouds with
            some evening light breaking through.

            A professional contractor in a dark navy blue jacket (color #1B4B8F) with
            a small house-and-hands logo emblem is walking toward the home carrying
            equipment, ready to assess emergency storm damage.

            The scene conveys urgency and reliability - help arriving when needed,
            even after hours.

            Setting: Indianapolis residential neighborhood, dramatic twilight sky,
            recent storm atmosphere.

            Style: Cinematic commercial photography, dramatic lighting, conveys
            reliability and immediate response.

            NO text, NO watermarks.""",
            "reference_images": [logo_path]
        }
    ]

    # Generate each image
    for img_config in images_to_generate:
        generate_image(
            prompt=img_config["prompt"],
            reference_images=img_config.get("reference_images"),
            aspect_ratio=img_config.get("aspect_ratio", "16:9"),
            image_size="2K",
            filename=img_config["filename"]
        )
        print()

if __name__ == "__main__":
    main()
