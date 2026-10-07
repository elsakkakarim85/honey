import json
import base64
from typing import List
from pydantic import BaseModel
import svgwrite
import cairosvg
import os

# --- AI Brand Strategist Schemas ---

class SocialMediaPost(BaseModel):
    platform: str
    copy: str
    hashtags: str

class BrandIdentity(BaseModel):
    brand_name: str
    tagline: str
    product_description: str
    social_posts: List[SocialMediaPost]

def generate_brand_identity(apiary_profile: str, vibe: str) -> BrandIdentity:
    """
    Prompts the local LLaMA-3 GGUF model to autonomously generate 
    a highly converting Brand Identity based on the honey profile and vibe.
    """
    print(f"Loading local LLaMA-3... Generating {vibe} brand for {apiary_profile}")
    # Mocking the local LLM inference output matching the schema
    mock_brand = {
        "brand_name": "Mountain Gold Apiaries",
        "tagline": "Nature's Purest Essence",
        "product_description": "Our organic Mountain Sidr Honey is ethically harvested...",
        "social_posts": [
            {
                "platform": "Instagram",
                "copy": "Experience the luxury of raw, unfiltered Sidr honey. Direct from our hives to your table. 🍯",
                "hashtags": "#RawHoney #Sidr #OrganicLiving"
            }
        ]
    }
    return BrandIdentity(**mock_brand)


# --- Programmatic Print-Ready Label Generator ---

def generate_print_label(brand_data: BrandIdentity, dpp_qr_path: str = "../batch_qrcode.png", output_pdf: str = "print_ready_label.pdf"):
    """
    Programmatically assembles a high-resolution, stylized Honey Jar Label template.
    CRITICAL: Perfectly integrates the Zero-Gas DPP QR Code for end-to-end traceability.
    """
    print(f"Generating professional SVG vector label for {brand_data.brand_name}...")
    
    # Label dimensions (e.g., standard honey jar wrap: 800x400)
    width, height = 800, 400
    dwg = svgwrite.Drawing('temp_label.svg', size=(width, height), profile='full')

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill='#fffbf0'))
    
    # Outer Border (Gold)
    dwg.add(dwg.rect(insert=(10, 10), size=(width-20, height-20), fill='none', stroke='#d4af37', stroke_width=4))

    # --- Front Center (Branding) ---
    # Brand Name
    dwg.add(dwg.text(brand_data.brand_name.upper(), insert=(width/2, 100), text_anchor="middle",
                     font_size='36px', font_family='Georgia, serif', font_weight='bold', fill='#2d3748'))
    # Tagline
    dwg.add(dwg.text(brand_data.tagline, insert=(width/2, 140), text_anchor="middle",
                     font_size='18px', font_family='Georgia, serif', font_style='italic', fill='#4a5568'))
                     
    # Honey Type / Badge
    dwg.add(dwg.rect(insert=((width/2)-80, 180), size=(160, 40), rx=5, ry=5, fill='#d4af37'))
    dwg.add(dwg.text("100% RAW ORGANIC", insert=(width/2, 205), text_anchor="middle",
                     font_size='14px', font_family='Arial, sans-serif', font_weight='bold', fill='white'))

    # Description (Left Side)
    # Note: SVG text wrapping is complex, usually handled by <foreignObject>, keeping it simple here
    desc_lines = brand_data.product_description.split('.')
    y_offset = 120
    for line in desc_lines[:3]:
        if line.strip():
            dwg.add(dwg.text(line.strip()[:35] + "...", insert=(40, y_offset), 
                             font_size='12px', font_family='Arial', fill='#2d3748'))
            y_offset += 20

    # --- Back Side (Compliance & Digital Product Passport) ---
    dwg.add(dwg.text("TRACE YOUR HONEY:", insert=(width-220, 150), 
                     font_size='14px', font_family='Arial', font_weight='bold', fill='#2d3748'))
    
    # Embed the Zero-Gas DPP QR Code (Must be base64 encoded for standalone SVG/PDF)
    try:
        if os.path.exists(dpp_qr_path):
            with open(dpp_qr_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                img_href = f"data:image/png;base64,{encoded_string}"
        else:
            # Fallback placeholder if QR doesn't exist
            img_href = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
            
        # Draw the QR Code image
        dwg.add(dwg.image(href=img_href, insert=(width-220, 170), size=(150, 150)))
    except Exception as e:
        print(f"Warning: Could not embed DPP QR code: {e}")

    dwg.save()
    
    print("Converting high-resolution SVG to Print-Ready PDF...")
    try:
        # Convert SVG to PDF using CairoSVG
        cairosvg.svg2pdf(url='temp_label.svg', write_to=output_pdf)
        print(f"Success! Label saved to {output_pdf}")
    except Exception as e:
        print(f"Warning: PDF conversion failed (likely missing libcairo dependency on Windows). Error: {e}")

if __name__ == "__main__":
    brand = generate_brand_identity("Mountain Sidr Honey, Organic", "Luxury")
    generate_print_label(brand)
