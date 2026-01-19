# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a vanilla HTML/CSS/JavaScript website for **Clear Choice Restoration**, a family-owned residential roofing and restoration company based in Indianapolis, IN. The site requires a custom "Meet the Staff" page with an admin interface for managing employee profiles.

## Company Information

- **Company Name:** Clear Choice Restoration, LLC
- **Website:** ccrroof.com
- **Address:** 195 N Shortridge Rd, Ste A, Indianapolis, IN 46219
- **Phone:** (317) 358-8630
- **Emergency/After Hours:** (317) 910-7605
- **Business Hours:** Monday-Friday, 9:00 AM - 5:00 PM
- **Established:** 2001 (Incorporated 2007)
- **Type:** Family-owned and operated

## Brand Colors (from logo)

The logo features a house cradled in hands with a two-color blue scheme:

| Color | Hex | Usage |
|-------|-----|-------|
| Dark Navy Blue | `#1B4B8F` | Primary - hands, window, text, buttons |
| Light Sky Blue | `#5BA4D4` | Secondary - roof outline, accents, hover states |
| White | `#FFFFFF` | Backgrounds, text on dark |
| Dark Gray | `#161616` | Header/footer backgrounds |
| Light Gray | `#F7F7F7` | Alternate section backgrounds |

## Services Offered

- **Roofing:** Replacement and repairs (metal & asphalt shingles)
- **Gutters:** Installation and repair
- **Siding:** Aluminum and vinyl
- **Interior Damage:** Repair and restoration
- **Water Mitigation:** 24-hour emergency service
- **Insurance Claim Assistance:** Full support from adjuster meeting to job completion

## Key Selling Points

- Family-owned and operated
- Free inspections
- Licensed, bonded, and insured
- Limited Lifetime workmanship warranty
- Trained insurance specialists on staff
- BBB accredited with 5-star rating
- "No job is too BIG or too small"
- 24-hour emergency service available

## Architecture

### Site Structure
```
/
├── index.html              # Homepage
├── about.html              # About Us page
├── services.html           # Services overview
├── staff.html              # Meet the Staff (dynamic)
├── gallery.html            # Project portfolio/gallery
├── testimonials.html       # Customer reviews
├── faq.html                # Frequently asked questions
├── contact.html            # Contact page with PHP form
├── admin/
│   ├── index.html          # Staff admin interface (password protected)
│   └── api.php             # Staff CRUD API endpoint
├── css/
│   └── styles.css          # Main stylesheet
├── js/
│   ├── main.js             # Site-wide JavaScript
│   └── staff-admin.js      # Admin page logic
├── data/
│   └── staff.json          # Staff data (server-side JSON)
├── uploads/
│   └── staff/              # Staff photo uploads
├── contact-handler.php     # Contact form processor
└── Images/
    ├── Logos/              # Brand logos
    └── Site/               # Generated site images
```

### Pages
| Page | File | Description |
|------|------|-------------|
| Home | `index.html` | Hero, services overview, CTA sections |
| About | `about.html` | Company history, values, family-owned story |
| Services | `services.html` | Roofing, gutters, siding, water mitigation |
| Staff | `staff.html` | Dynamic team member display |
| Gallery | `gallery.html` | Portfolio of completed projects |
| Testimonials | `testimonials.html` | Customer reviews |
| FAQ | `faq.html` | Common questions and answers |
| Contact | `contact.html` | Form + contact info + map |
| Admin | `admin/index.html` | Staff management (password protected) |

### Staff Management System

Server-side PHP + JSON storage (for SiteGround hosting):
- **PHP API** (`admin/api.php`) handles CRUD operations
- **JSON file** (`data/staff.json`) stores staff data persistently
- **Photo uploads** saved to `uploads/staff/` directory
- **Simple password protection** via JavaScript prompt
- Staff page fetches and renders from JSON dynamically

Staff data structure:
```json
{
  "staff": [
    {
      "id": "unique-id",
      "name": "Employee Name",
      "title": "Job Title",
      "bio": "Employee bio text...",
      "photo": "uploads/staff/filename.jpg",
      "order": 1
    }
  ]
}
```

### Contact Form
PHP form handler (`contact-handler.php`) for SiteGround:
- Validates input server-side
- Sends email to company
- Returns success/error response
- Optional: saves to log file

## Development

### Local Development
For PHP functionality, use a local PHP server:
```bash
# PHP built-in server
php -S localhost:8000

# Or just open HTML files for static content testing
```

### Deployment (SiteGround)
1. Upload all files via FTP or File Manager
2. Ensure `data/` and `uploads/` directories are writable (755)
3. Update email address in `contact-handler.php`
4. Change admin password in `admin/index.html`

### No Build Process
Vanilla HTML/CSS/JS/PHP - no build tools required.

## Image Generation

### Model & Skill
- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro - newest/best quality)
- **Skill:** Use `gemini-image-generation` skill for API usage reference
- **API Key:** Use the Google AI key from global CLAUDE.md

### Generation Settings
```python
# Recommended settings for this project
model = "gemini-3-pro-image-preview"
image_size = "2K"  # High quality
aspect_ratios = {
    "hero_banner": "21:9",    # Wide cinematic
    "site_photos": "16:9",    # Standard landscape
    "about_photos": "3:2",    # Portrait-friendly
    "logos": "1:1"            # Square
}
```

### Brand Requirements for Generated Images
When generating images with people/workers:
- **Shirt color:** Dark navy blue (`#1B4B8F`)
- **Logo on uniforms:** House-in-hands symbol in light blue (`#6BA3D4`) on chest or back
- **Setting:** Indianapolis, IN - Midwestern residential neighborhoods
- **Context:** Hail damage, storm damage, roofing work

### Prompt Guidelines
Always include in prompts:
1. "Indianapolis" or "Midwestern residential neighborhood" for location context
2. Brand colors for any uniforms: "dark navy blue polo shirt (color #1B4B8F)"
3. Logo description: "house shape cradled by two hands in light blue (#6BA3D4)"
4. "NO text, NO watermarks" to keep images clean
5. Reference the logo symbol file when generating images with people

### Example Generation Code
```python
from pathlib import Path
import requests, json, base64

API_KEY = "AIzaSyA8AVfoNKfSyy9Nkpp9gOv_X1qdeSttUQE"
MODEL = "gemini-3-pro-image-preview"
LOGO_PATH = Path("Images/Logos/CCR_House_Hands_2C (1).jpg")

def generate_image(prompt, reference_images=None, aspect_ratio="16:9"):
    parts = [{"text": prompt}]
    if reference_images:
        for img in reference_images:
            with open(img, 'rb') as f:
                parts.append({"inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(f.read()).decode()
                }})

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{"parts": parts}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {"aspectRatio": aspect_ratio, "imageSize": "2K"}
            }
        }
    )
    # Extract image from response...
```

### Valid Aspect Ratios
`1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

## Generated Assets

### Logos (`Images/Logos/`)
| File | Description |
|------|-------------|
| `CCR_House_Hands_2C (1).jpg` | Original symbol only (house in hands) |
| `LOGO (4).pdf` | Original text only ("Clear Choice Restoration") |
| `CCR_Combined_Logo_Horizontal.png` | Generated combined logo (21:9 aspect) |
| `CCR_Combined_Logo_Stacked.png` | Generated stacked logo (1:1 aspect) |

### Site Images (`Images/Site/`)
| File | Usage | Description |
|------|-------|-------------|
| `hero-banner.jpg` | Homepage hero | Indianapolis home with new roof, skyline in background (21:9) |
| `roofing-team.jpg` | About/Team | Three team members in branded polos (16:9) |
| `hail-damage-inspection.jpg` | Services | Inspector marking hail damage on roof (16:9) |
| `storm-damage-roof.jpg` | Services | Close-up of hail-damaged shingles (16:9) |
| `new-roof-installation.jpg` | Services | Workers installing shingles (16:9) |
| `gutter-installation.jpg` | Services | Gutter installation work (16:9) |
| `siding-work.jpg` | Services | Vinyl siding installation (16:9) |
| `free-inspection.jpg` | CTA sections | Consultant meeting homeowners (16:9) |
| `emergency-service.jpg` | 24hr service | Truck arriving at dusk, dramatic sky (16:9) |
| `about-family-business.jpg` | About page | Team in office reviewing plans (3:2) |

All images feature brand colors and logo on uniforms where people appear.

## External Resources

- **BBB Profile:** https://www.bbb.org/us/in/indianapolis/profile/general-contractor/clear-choice-restoration-llc-0382-90017401
- **Yelp:** https://www.yelp.com/biz/clear-choice-restoration-indianapolis
- **Facebook:** Linked from main site
- **Logo Files:** Located in `Images/Logos/`
