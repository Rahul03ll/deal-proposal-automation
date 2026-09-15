import sys
import struct

def encode_lzw(data, min_code_size):
    clear_code = 1 << min_code_size
    end_code = clear_code + 1
    code_size = min_code_size + 1
    next_code = end_code + 1
    max_code = (1 << code_size)

    dictionary = {bytes([i]): i for i in range(clear_code)}
    
    bits = 0
    bit_count = 0
    output = bytearray()
    
    def write_bits(val, n):
        nonlocal bits, bit_count, output
        bits |= (val << bit_count)
        bit_count += n
        while bit_count >= 8:
            output.append(bits & 0xFF)
            bits >>= 8
            bit_count -= 8

    write_bits(clear_code, code_size)
    
    pattern = bytearray()
    for byte in data:
        pattern.append(byte)
        pat_bytes = bytes(pattern)
        if pat_bytes in dictionary:
            continue
        
        # Output code for pattern[:-1]
        write_bits(dictionary[bytes(pattern[:-1])], code_size)
        
        if next_code < 4096:
            dictionary[pat_bytes] = next_code
            next_code += 1
            if next_code > max_code and code_size < 12:
                code_size += 1
                max_code = (1 << code_size)
        else:
            write_bits(clear_code, code_size)
            code_size = min_code_size + 1
            max_code = (1 << code_size)
            next_code = end_code + 1
            dictionary = {bytes([i]): i for i in range(clear_code)}
            
        pattern = bytearray([byte])
        
    if pattern:
        write_bits(dictionary[bytes(pattern)], code_size)
        
    write_bits(end_code, code_size)
    if bit_count > 0:
        output.append(bits & 0xFF)
        
    # Chunk into 255-byte sub-blocks
    result = bytearray()
    result.append(min_code_size)
    idx = 0
    while idx < len(output):
        chunk = output[idx:idx+255]
        result.append(len(chunk))
        result.extend(chunk)
        idx += len(chunk)
    result.append(0) # Block terminator
    return result

def create_gif(frames_indices, width, height, palette, delay_cs=250):
    # Palette is flat list of RGB (768 bytes)
    gif = bytearray(b"GIF89a")
    # Screen descriptor
    gif.extend(struct.pack("<HHBBB", width, height, 0x80 | 0x70 | 0x07, 0, 0))
    # Global palette (256 * 3 bytes)
    gif.extend(palette)
    
    # Netscape loop extension
    gif.extend(b"\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00")
    
    for frame_data in frames_indices:
        # Graphic Control Extension
        # delay_cs is in 1/100s (e.g. 250 = 2.5s)
        gif.extend(struct.pack("<BBBBHB", 0x21, 0xF9, 0x04, 0x00, delay_cs, 0x00))
        gif.append(0) # terminator
        
        # Image Descriptor
        gif.extend(struct.pack("<BHHHHB", 0x2C, 0, 0, width, height, 0x00))
        
        # LZW image data
        lzw_data = encode_lzw(frame_data, 8)
        gif.extend(lzw_data)
        
    gif.append(0x3B) # Trailer
    return bytes(gif)

print("GIF Encoder module loaded")
