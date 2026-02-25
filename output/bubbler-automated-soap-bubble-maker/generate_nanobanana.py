#!/usr/bin/env python3
"""Generate Bubbler illustration using Google Gemini Nano Banana (image generation)."""

import os
import sys
from pathlib import Path
from google import genai
from google.genai import types

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE_1 = SCRIPT_DIR / "cross_section_illustration_bubbler.png"
OUTPUT_FILE_2 = SCRIPT_DIR / "isometric_illustration_bubbler.png"

API_KEY = "YOUR API KEY"

CROSS_SECTION_PROMPT = """Create a detailed technical SIDE CROSS-SECTION illustration of an automated soap bubble machine called "Bubbler". Engineering cutaway style, clean labels, white background.

The device viewed from the side (looking along its long axis):
- FLAT BASE PLATE at the bottom (215x206mm footprint) with 4 rubber leveling feet at corners
- On top of the base: a SHALLOW OVAL VAT (200x170mm, 20mm deep) filled with blue-tinted soap solution
- On the RIGHT SIDE: a TAPERED ENCLOSURE PROTRUSION (inverse-U rim) — wide at the base (~80mm), narrowing to ~60mm at the top. This protrusion is cut away to reveal internal components stacked vertically:
  - Near the base: 4xAA BATTERY HOLDER (2x2 flat arrangement)
  - Above batteries: MAIN PCB (50x35mm, green circuit board with labeled chips: MCU, HX711, H-bridge)
  - At shaft height: small GEARED DC MOTOR
  - Near the top: flat CENTRIFUGAL BLOWER FAN (40x40x10mm)
  - An L-SHAPED AIR DUCT from the fan bending 90° to exit horizontally through a round 40mm outlet
- LEFT SIDE of rim is minimal (~15mm above vat)
- A ROTATING SHAFT spans across the top of the vat, with a small pivot bearing on each side
- From the shaft, a 30mm WAND ARM extends left, with a 160mm FLEXIBLE WIRE LOOP at the end shown as a vertical line (edge-on view) standing upright above the vat (blow position)
- A DASHED ARC shows the loop's rotation path: ~175° from vertical (upright, blow position) sweeping down-left into the vat (dip position)
- The AIR DUCT EXIT is horizontally aligned with the center of the upright loop
- A small STRAIN GAUGE shown bonded near the shaft bearing
- Label every component clearly with leader lines

Style: Technical product illustration, clean engineering cutaway, precise proportions, white/light background, colored components (blue for mechanical, orange for electronics, green for PCB, gray for enclosure)."""

ISOMETRIC_PROMPT = """Create a photorealistic ISOMETRIC PRODUCT CONCEPT illustration of an automated soap bubble machine called "Bubbler" on a wooden outdoor table in a sunny park setting.

The device is a compact tabletop machine (~215x206mm footprint, ~250mm tall):
- A flat rectangular BASE in matte dark gray plastic with small rubber feet
- On top: an OPEN OVAL VAT filled with iridescent soap solution (shimmering rainbow surface)
- On one long side: a TAPERED HOUSING/PROTRUSION in dark gray plastic — wider at the base, narrowing toward the top, with subtle ventilation grilles and two small buttons (one green LED glowing)
- Rising from the top of the housing: a thin metal WAND ARM with a large circular WIRE LOOP (160mm diameter) standing upright above the vat
- A large, beautiful SOAP BUBBLE (~400mm) being inflated from the loop, catching rainbow light refractions
- The round air duct outlet visible on the housing, pointing at the loop center
- Clean, modern consumer product design — think Apple-like simplicity in dark gray/charcoal plastic
- Outdoor setting: wooden picnic table, green grass, warm afternoon sunlight, maybe a child's hand reaching toward the bubble in the background (blurred)

Style: Photorealistic product rendering, warm natural lighting, shallow depth of field on background."""


def generate_image(client, prompt, output_path):
    """Generate an image using Gemini's image generation."""
    print(f"Generating: {output_path.name}...")

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_bytes = part.inline_data.data
            output_path.write_bytes(image_bytes)
            size_kb = len(image_bytes) / 1024
            print(f"Saved: {output_path} ({size_kb:.0f} KB)")
            return True
        elif part.text is not None:
            print(f"Text response: {part.text[:200]}")

    print("ERROR: No image in response")
    return False


def main():
    print("=" * 60)
    print("Bubbler — Nano Banana Image Generation")
    print("=" * 60)

    client = genai.Client(api_key=API_KEY)

    # Generate cross-section
    success1 = generate_image(client, CROSS_SECTION_PROMPT, OUTPUT_FILE_1)

    # Generate isometric concept
    success2 = generate_image(client, ISOMETRIC_PROMPT, OUTPUT_FILE_2)

    if success1 and success2:
        print("\nBoth images generated successfully.")
    elif success1 or success2:
        print("\nOne image generated.")
    else:
        print("\nFailed to generate images.")
        sys.exit(1)


if __name__ == "__main__":
    main()
