# import os
# import re

# def format_duration(seconds):
#     # Helper function to format the time into SRT format (HH:MM:SS,SSS)
#     hours = int(seconds // 3600)
#     minutes = int((seconds % 3600) // 60)
#     seconds = int(seconds % 60)
#     milliseconds = int((seconds % 1) * 1000)
#     return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# def read_srt_file(srt_file):
#     """Reads an SRT file and returns its contents as a list of segments."""
#     segments = []
#     with open(srt_file, "r") as file:
#         content = file.read().strip()
#         entries = content.split("\n\n")
        
#         for entry in entries:
#             lines = entry.splitlines()
#             idx = int(lines[0])
#             time_range = lines[1]
#             text = "\n".join(lines[2:])
            
#             # Parse start and end times
#             start_time, end_time = time_range.split(" --> ")
#             start_time = start_time.strip()
#             end_time = end_time.strip()
            
#             segments.append({
#                 "index": idx,
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "text": text
#             })
#     return segments

# def adjust_timestamps_and_stitch(segments_list):
#     """Adjust timestamps to create a continuous flow and combine all segments."""
#     combined_segments = []
#     current_end_time = "00:00:00,000"  # Start at 00:00:00,000
    
#     for segments in segments_list:
#         for segment in segments:
#             start_time = segment["start_time"]
#             end_time = segment["end_time"]
#             text = segment["text"]
            
#             # Update the start time to match the previous segment's end time
#             if start_time != "00:00:00,000" and start_time != current_end_time:
#                 start_time = current_end_time

#             # Update the end time to the current segment's end time
#             current_end_time = end_time

#             combined_segments.append({
#                 "start_time": start_time,
#                 "end_time": end_time,
#                 "text": text
#             })
    
#     return combined_segments

# def write_combined_srt(combined_segments, output_file):
#     """Writes the combined SRT segments to a new SRT file."""
#     with open(output_file, "w") as file:
#         for idx, segment in enumerate(combined_segments, 1):
#             file.write(f"{idx}\n")
#             file.write(f"{segment['start_time']} --> {segment['end_time']}\n")
#             file.write(f"{segment['text']}\n\n")

# def stitch_srt_files(input_folder, output_file):
#     """Stitches all SRT files in the input folder into a single output SRT file."""
#     all_segments = []
    
#     # Read all SRT files in the folder
#     for file_name in os.listdir(input_folder):
#         if file_name.endswith(".srt"):
#             file_path = os.path.join(input_folder, file_name)
#             segments = read_srt_file(file_path)
#             all_segments.append(segments)
    
#     # Adjust timestamps and stitch together
#     combined_segments = adjust_timestamps_and_stitch(all_segments)
    
#     # Write the combined SRT file
#     write_combined_srt(combined_segments, output_file)

import os
import re
from datetime import timedelta

def format_duration(seconds):
    # Helper function to format the time into SRT format (HH:MM:SS,SSS)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def read_srt_file(srt_file):
    """Reads an SRT file and returns its contents as a list of segments."""
    segments = []
    with open(srt_file, "r") as file:
        content = file.read().strip()
        entries = content.split("\n\n")
        
        for entry in entries:
            lines = entry.splitlines()
            idx = int(lines[0])
            time_range = lines[1]
            text = "\n".join(lines[2:])
            
            # Parse start and end times
            start_time, end_time = time_range.split(" --> ")
            start_time = start_time.strip()
            end_time = end_time.strip()
            
            segments.append({
                "index": idx,
                "start_time": start_time,
                "end_time": end_time,
                "text": text
            })
    return segments

def parse_srt_time(srt_time):
    """Convert SRT timestamp (HH:MM:SS,SSS) to timedelta."""
    hours, minutes, seconds = map(int, srt_time.split(":"))
    seconds, milliseconds = divmod(seconds, 1000)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def format_srt_time(td):
    """Convert timedelta to SRT timestamp (HH:MM:SS,SSS)."""
    total_seconds = int(td.total_seconds())
    milliseconds = td.microseconds // 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def adjust_timestamps_and_stitch(segments_list):
    """Adjust timestamps to create continuous flow across multiple SRT files."""
    combined_segments = []
    cumulative_offset = timedelta()  # Track the cumulative offset
    
    for segments in segments_list:
        for segment in segments:
            start_time = parse_srt_time(segment["start_time"]) + cumulative_offset
            end_time = parse_srt_time(segment["end_time"]) + cumulative_offset
            
            combined_segments.append({
                "start_time": format_srt_time(start_time),
                "end_time": format_srt_time(end_time),
                "text": segment["text"]
            })
        
        # Update cumulative offset with the duration of the current SRT file
        if segments:
            last_segment = segments[-1]
            cumulative_offset = parse_srt_time(last_segment["end_time"])
    
    return combined_segments


def write_combined_srt(combined_segments, output_file):
    """Writes the combined SRT segments to a new SRT file."""
    with open(output_file, "w") as file:
        for idx, segment in enumerate(combined_segments, 1):
            file.write(f"{idx}\n")
            file.write(f"{segment['start_time']} --> {segment['end_time']}\n")
            file.write(f"{segment['text']}\n\n")

def stitch_srt_files(input_folder, output_file):
    """Stitches all SRT files in the input folder into a single output SRT file."""
    all_segments = []
    
    # Read all SRT files in the folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".srt"):
            file_path = os.path.join(input_folder, file_name)
            segments = read_srt_file(file_path)
            all_segments.append(segments)
    
    # Adjust timestamps and stitch together
    combined_segments = adjust_timestamps_and_stitch(all_segments)
    
    # Write the combined SRT file
    write_combined_srt(combined_segments, output_file)