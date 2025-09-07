from PIL import Image, ImageSequence
import os

gif_path = "tumblr_m6gygdxAn31roaheko1_500.gif" # gif path here example one already set

# Get the current workspace directory (where this script is located)
workspace_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(workspace_dir, "converted_frames")
preview_gif_path = os.path.join(output_folder, "preview.gif")

os.makedirs(output_folder, exist_ok=True)

gif = Image.open(gif_path)
processed_frames = []

for i, frame in enumerate(ImageSequence.Iterator(gif)):
    # Convert to black and white (1-bit)
    bw_frame = frame.convert("1")
    
    # Resize to higher resolution, e.g., 256x128
    bw_frame = bw_frame.resize((128, 64)) #change to higher quality here
    
    # Save as XBM
    frame_filename = f"frame_{i:03d}.xbm"
    bw_frame.save(os.path.join(output_folder, frame_filename))
    
    processed_frames.append(bw_frame)
    print(f"Saved {frame_filename}")

print(f"Saved {i+1} frames to {output_folder}")

def save_preview_gif(frames, path, duration=gif.info.get("duration", 100)):
    # Save frames as a preview GIF
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    print(f"Preview GIF saved as {path}")

if processed_frames:
    save_preview_gif(processed_frames, preview_gif_path)
