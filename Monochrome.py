import re
import os
from PIL import Image

input_folder = r"converted_frames"
output_file = r"all_frames.h"
preview_gif = r"preview.gif"

pattern = re.compile(
    r"static char im_bits\[\] = \{([^}]*)\};",
    re.DOTALL
)

all_arrays = []
frames_for_gif = []

xbm_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.xbm')])

for i, filename in enumerate(xbm_files):
    filepath = os.path.join(input_folder, filename)
    with open(filepath, 'r') as f:
        content = f.read()
        
        match = pattern.search(content)
        if not match:
            print(f"Warning: no array found in {filename}")
            continue
        
        array_content = match.group(1).strip()
        # Rename the array variable to a unique name, e.g. frame_000_bits
        array_name = f"frame_{i:03d}_bits"
        
        array_declaration = f"static const char {array_name}[] PROGMEM = {{\n{array_content}\n}};\n"
        all_arrays.append(array_declaration)

    # Load image for GIF preview
    try:
        img = Image.open(filepath)
        img = img.convert("1")  # Ensure monochrome
        frames_for_gif.append(img)
    except Exception as e:
        print(f"Could not load {filename} for GIF: {e}")

with open(output_file, 'w') as f_out:
    f_out.write("// Combined XBM frames\n\n")
    f_out.write("#include <Arduino.h>\n")
    f_out.write("#include <avr/pgmspace.h>\n\n")
    for array_code in all_arrays:
        # Add defines before each frame
        f_out.write("#define im_width 256\n#define im_height 128\n")
        f_out.write(array_code)
        f_out.write("\n")

# Save preview GIF
if frames_for_gif:
    frames_for_gif[0].save(
        preview_gif,
        save_all=True,
        append_images=frames_for_gif[1:],
        duration=100,
        loop=0
    )
    print(f"Preview GIF saved as {preview_gif}")
else:
    print("No frames available for GIF preview.")

print(f"Combined {len(all_arrays)} frames into {output_file}")
