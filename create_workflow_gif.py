#!/usr/bin/env python3
"""
Compile generated high-res workflow screenshots into a seamless animated GIF.
Target size: 960x540 for optimal Substack / web viewing.
"""

import os
from PIL import Image, ImageOps

BRAIN_DIR = r"C:\Users\KIIT\.gemini\antigravity\brain\9c77df73-1e61-457c-ba52-ded39d2152c9"
OUTPUT_GIF_BRAIN = os.path.join(BRAIN_DIR, "workflow_demo.gif")
OUTPUT_GIF_SCRATCH = os.path.join(r"C:\Users\KIIT\.gemini\antigravity\scratch\deal_proposal_automation", "workflow_demo.gif")

image_files = [
    os.path.join(BRAIN_DIR, "sheet_tracker_view_1789486920181.jpg"),
    os.path.join(BRAIN_DIR, "editor_code_view_1789486980332.jpg"),
    os.path.join(BRAIN_DIR, "terminal_run_view_1789487031031.jpg"),
    os.path.join(BRAIN_DIR, "proposal_sow_doc_1789487194826.jpg"),
    os.path.join(BRAIN_DIR, "telegram_mobile_card_1789487102361.jpg")
]

target_w, target_h = 960, 540
processed_frames = []

for idx, p in enumerate(image_files):
    if not os.path.exists(p):
        print(f"[!] Warning: Image {p} not found!")
        continue
    img = Image.open(p).convert("RGB")
    
    # Scale to fit with padding if aspect ratio differs (especially for the 9:16 mobile telegram card)
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    
    if abs(img_ratio - target_ratio) > 0.1:
        # Pad with pleasant dark background
        scaled = ImageOps.contain(img, (target_w, target_h), method=Image.Resampling.LANCZOS)
        frame = Image.new("RGB", (target_w, target_h), "#0E1621" if "telegram" in p else "#1E1E1E")
        offset = ((target_w - scaled.width) // 2, (target_h - scaled.height) // 2)
        frame.paste(scaled, offset)
    else:
        frame = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
    # Convert to adaptive 256 color palette for clean GIF compression
    frame_p = frame.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    processed_frames.append(frame_p)

if processed_frames:
    # Durations in ms: [Sheet: 2.2s, Editor: 2.0s, Terminal: 2.5s, SOW Doc: 3.0s, Telegram: 2.5s]
    durations = [2200, 2000, 2500, 3200, 2600]
    
    # Save to brain directory
    processed_frames[0].save(
        OUTPUT_GIF_BRAIN,
        save_all=True,
        append_images=processed_frames[1:],
        duration=durations[:len(processed_frames)],
        loop=0,
        optimize=True
    )
    print(f"[✓] Successfully compiled animated GIF at: {OUTPUT_GIF_BRAIN}")
    
    # Also save to scratch
    processed_frames[0].save(
        OUTPUT_GIF_SCRATCH,
        save_all=True,
        append_images=processed_frames[1:],
        duration=durations[:len(processed_frames)],
        loop=0,
        optimize=True
    )
    print(f"[✓] Also saved to: {OUTPUT_GIF_SCRATCH}")
else:
    print("[!] No frames to compile!")
