import os
import re
from datetime import timedelta

def parse_timestamp(timestamp):
    """Convert SRT timestamp to timedelta."""
    hours, minutes, seconds = map(float, re.split('[:,]', timestamp))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def format_timestamp(td):
    """Convert timedelta back to SRT timestamp format."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def adjust_srt_timestamps(input_folder, output_file):
    """Combine SRT files in the folder, adjusting timestamps sequentially."""
    srt_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.srt')])
    combined_subtitles = []
    current_offset = timedelta()
    subtitle_counter = 1

    for srt_file in srt_files:
        with open(os.path.join(input_folder, srt_file), 'r', encoding='utf-8') as file:
            content = file.read()

        entries = re.split(r'\n\n+', content.strip())
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 2:
                # Extract index and timestamp
                index = subtitle_counter
                timestamp_line = lines[1]
                start, end = map(str.strip, timestamp_line.split('-->'))
                adjusted_start = format_timestamp(parse_timestamp(start) + current_offset)
                adjusted_end = format_timestamp(parse_timestamp(end) + current_offset)

                # Combine adjusted entry
                combined_entry = f"{index}\n{adjusted_start} --> {adjusted_end}\n" + "\n".join(lines[2:])
                combined_subtitles.append(combined_entry)

                subtitle_counter += 1

        # Update offset for the next file
        if entries:
            last_entry = entries[-1]
            last_timestamp_line = last_entry.split('\n')[1]
            last_end_time = last_timestamp_line.split('-->')[1].strip()
            current_offset = parse_timestamp(last_end_time) + current_offset

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(combined_subtitles))


# Example usage
folder_path = "Swami_DJ_audio_output_audio_segment_files_srt"
output_path = "Swami_DJ_audio_output_audio_segment_files_srt/combined_file.srt"
adjust_srt_timestamps(folder_path, output_path)


# # Example usage
# combine_srt_files(folder_path="Swami_DJ_audio_output_audio_segment_files_srt", output_file="Swami_DJ_audio_output_audio_segment_files_srt/combined_output.srt")
