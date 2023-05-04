import re
import os

# Regex pattern to match timestamps in the format of "minute:second" or "hour:minute:second"
timestamp_pattern = r'(\d+:)?\d+:\d+'

# Prompt user for timestamps file
ts_file = input("Enter path to timestamps: ")

with open(ts_file, 'r') as file:
    lines = [line.rstrip() for line in file]
    timestamps_dict = {}
    for line in lines:
        # Check if the line matches timestamp regex
        match = re.search(timestamp_pattern, line)
        if match:
            timestamp = match.group(0)
            # Remove the timestamp, parentheses, and period from the line
            line_without_ts = re.sub(timestamp_pattern, '', line).strip(' ()')
            line_without_ts = line_without_ts.replace('. ', '-')
            line_without_ts = line_without_ts.replace(' ', '_')
            line_without_ts = line_without_ts.replace('.', '-')
            # Add the timestamp and line to the dictionary
            timestamps_dict[line_without_ts] = timestamp

for k, v in timestamps_dict.items():
    print(k, v)

print("--- Timestamps ---")

# Create a folder for the generated clips
if not os.path.exists("Generated Clips"):
    os.makedirs("Generated Clips")

os.chdir("Generated Clips")

# Create a file with the exported timestamps
with open('ExportedTimestampsFromScript.txt', 'w') as f:
    f.write('\n'.join(timestamps_dict))

# Prompt user for media file
media_file = input("Enter path to media file: ")
print("Media file grabbed: ", media_file)

# Create clips using the timestamps
for i, timestamp_key in enumerate(timestamps_dict.keys()):
    start_time = timestamps_dict[timestamp_key]
    end_time = timestamps_dict[list(timestamps_dict.keys())[i+1]] if i < len(timestamps_dict)-1 else None
    clip_name = f"{timestamp_key}.mp4"  # Change to .mp3 if necessary
    clip_path = os.path.join("Generated Clips", clip_name)
    cmd = f"ffmpeg -i {media_file} -ss {start_time}{' -to '+end_time if end_time else ''} -c copy {clip_name}"
    os.system(cmd)
