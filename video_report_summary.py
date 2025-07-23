
import os
import csv
import datetime
import re

base_dir = r"C:/Users/LeeEunseo/Documents/GitHub/video-speed-tool/Fast_Forward_Videos"
folders = {
    "1x": r"C:/Users/LeeEunseo/Documents/GitHub/video-speed-tool/2025-07-22",
    "2x": os.path.join(base_dir, "Videos_2x"),
    "4x": os.path.join(base_dir, "Videos_4x"),
    "8x": os.path.join(base_dir, "Videos_8x"),
    "16x": os.path.join(base_dir, "Videos_16x")
}

def latest_subfolder(path):
    try:
        subs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return os.path.join(path, sorted(subs)[-1]) if subs else None
    except:
        return None

for k in ["2x", "4x", "8x", "16x"]:
    latest = latest_subfolder(folders[k])
    if latest:
        folders[k] = latest

def extract_group_name(filename):
    base = os.path.splitext(filename)[0]
    group = re.split(r"_\d*x", base)[0]
    return group + "~"

size_data = {}
for label, path in folders.items():
    if not os.path.exists(path):
        continue
    for f in os.listdir(path):
        if f.lower().endswith(".mp4"):
            group = extract_group_name(f)
            size = os.path.getsize(os.path.join(path, f)) / (1024 * 1024)
            size_data.setdefault(group, {})[label] = round(size, 2)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
csv_file = os.path.join(base_dir, f"converted_video_sizes_report_{timestamp}.csv")

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Filename", "1x (MB)", "2x (MB)", "4x (MB)", "8x (MB)", "16x (MB)"])
    for group in sorted(size_data):
        row = [group] + [size_data[group].get(x, "") for x in ["1x", "2x", "4x", "8x", "16x"]]
        writer.writerow(row)

print(f"\n CSV file saved: {csv_file}")
