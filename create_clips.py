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

print("--- Timestamps ---")
for k, v in timestamps_dict.items():
    print(k, v)

# Create a folder for the generated clips
if not os.path.exists("Generated Clips"):
    os.makedirs("Generated Clips")

# Navigate to directory to export. Could also add the path to
# the export command, not sure what is cleaner
os.chdir("Generated Clips")

# Create a file with the exported timestamps
with open('ExportedTimestampsFromScript.txt', 'w') as f:
    for key, value in timestamps_dict.items():
        f.write(f'{key}: {value}\n')

# Prompt user for media file
media_file = input("Enter path to media file: ")
print("Media file grabbed: ", media_file)

extension = media_file[-3:]
print("Extension of file: ", extension)

# Create clips using the timestamps
for i, timestamp_key in enumerate(timestamps_dict.keys()):
    start_time = timestamps_dict[timestamp_key]
    end_time = timestamps_dict[list(timestamps_dict.keys())[i+1]] if i < len(timestamps_dict)-1 else None
    clip_name = f"{timestamp_key}.{extension}"
    clip_path = os.path.join("Generated Clips", clip_name)
    cmd = f"ffmpeg -i {media_file} -ss {start_time}{' -to '+end_time if end_time else ''} -c copy {clip_name}"
    os.system(cmd)
