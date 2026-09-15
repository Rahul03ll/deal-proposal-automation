import os
import struct
from lzw_gif import create_gif

BRAIN_DIR = r"C:\Users\KIIT\.gemini\antigravity\brain\9c77df73-1e61-457c-ba52-ded39d2152c9"
SCRATCH_DIR = r"C:\Users\KIIT\.gemini\antigravity\scratch\deal_proposal_automation"
FRAMES_DIR = os.path.join(SCRATCH_DIR, "raw_frames")

# Create 216-color standard 6x6x6 color cube + 40 grayscales
palette_bytes = bytearray()
for r in [0, 51, 102, 153, 204, 255]:
    for g in [0, 51, 102, 153, 204, 255]:
        for b in [0, 51, 102, 153, 204, 255]:
            palette_bytes.extend([r, g, b])
# Fill remaining 40 slots with grayscale ramp
for i in range(40):
    val = int(i * 255 / 39)
    palette_bytes.extend([val, val, val])

def read_bmp(path):
    with open(path, "rb") as f:
        data = f.read()
    # BMP header: offset 10 gives pixel data start, offset 18 gives width, offset 22 gives height
    offset = struct.unpack("<I", data[10:14])[0]
    width, height = struct.unpack("<ii", data[18:26])
    row_size = ((width * 3 + 3) // 4) * 4
    
    indices = bytearray(width * height)
    # BMP is stored bottom-to-top
    for y in range(height):
        src_y = height - 1 - y
        row_start = offset + src_y * row_size
        for x in range(width):
            b = data[row_start + x*3]
            g = data[row_start + x*3 + 1]
            r = data[row_start + x*3 + 2]
            
            # Map RGB to 6x6x6 cube index
            ri = round(r / 51)
            gi = round(g / 51)
            bi = round(b / 51)
            idx = ri * 36 + gi * 6 + bi
            indices[y * width + x] = idx
            
    return indices, width, height

print("[*] Reading BMP frames...")
frame_indices = []
w, h = 800, 450
for i in range(4):
    f_path = os.path.join(FRAMES_DIR, f"frame_{i}.bmp")
    idx_data, fw, fh = read_bmp(f_path)
    frame_indices.append(idx_data)
    w, h = fw, fh
    print(f"   [+] Loaded frame {i} ({fw}x{fh})")

print("[*] Encoding animated GIF with LZW compression...")
# 250 = 2.5 seconds per frame
gif_data = create_gif(frame_indices, w, h, palette_bytes, delay_cs=250)

# Save to brain
brain_gif = os.path.join(BRAIN_DIR, "workflow_demo.gif")
with open(brain_gif, "wb") as f:
    f.write(gif_data)
print(f"[OK] Saved animated GIF to: {brain_gif} ({len(gif_data)/1024:.1f} KB)")

# Save to scratch
scratch_gif = os.path.join(SCRATCH_DIR, "workflow_demo.gif")
with open(scratch_gif, "wb") as f:
    f.write(gif_data)
print(f"[OK] Saved animated GIF to: {scratch_gif}")
