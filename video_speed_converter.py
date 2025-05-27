
import os
from moviepy.editor import VideoFileClip, vfx
import datetime

# Folder paths
raw_base = r"C:/Users/LeeEunseo/Desktop/영상 배속 적용/Videos_raw"
def latest_subfolder(path):
    try:
        subs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return os.path.join(path, sorted(subs)[-1]) if subs else None
    except:
        return None

raw_folder = latest_subfolder(raw_base)

base_output_folder = r"C:/Users/LeeEunseo/Desktop/video-speed-too/Fast_Forward_Videos"
output_base_names = {
    2: "Videos_2x",
    4: "Videos_4x",
    8: "Videos_8x",
    16: "Videos_16x"
}

timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
output_folders = {}
for speed, base_name in output_base_names.items():
    folder = os.path.join(base_output_folder, base_name, timestamp_str)
    os.makedirs(folder, exist_ok=True)
    output_folders[speed] = folder

def process_video_speed(input_path, output_path, speed_factor):
    clip = VideoFileClip(input_path)
    sped_up_clip = clip.fx(vfx.speedx, speed_factor)
    sped_up_clip.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        preset='fast',
        bitrate='6000k',
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        threads=4,
        logger=None
    )
    clip.close()
    sped_up_clip.close()

success_count, fail_count = 0, 0
for filename in os.listdir(raw_folder):
    if filename.lower().endswith(".mp4"):
        input_path = os.path.join(raw_folder, filename)
        name_only = os.path.splitext(filename)[0]
        print(f"Processing: {filename}")
        for speed in output_folders:
            output_name = f"{name_only}_{speed}x.mp4"
            output_path = os.path.join(output_folders[speed], output_name)
            try:
                process_video_speed(input_path, output_path, speed)
                print(f"  → Saved {speed}x version to: {output_path}")
                success_count += 1
            except Exception as e:
                print(f"  [Error] {filename}, {speed}x: {e}")
                fail_count += 1

print("\n All video speed conversions are complete.")
print(f" Successful conversions: {success_count}")
print(f" Failed conversions: {fail_count}")
