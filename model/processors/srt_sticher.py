# import re
# from datetime import datetime, timedelta

# # Function to adjust SRT timestamps
# def adjust_timestamp(srt, offset):
#     adjusted_srt = []
#     time_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})')
    
#     for line in srt:
#         match = time_pattern.search(line)
#         if match:
#             start_time = datetime.strptime(f'{match.group(1)}:{match.group(2)}:{match.group(3)}.{match.group(4)}', '%H:%M:%S.%f')
#             end_time = datetime.strptime(f'{match.group(5)}:{match.group(6)}:{match.group(7)}.{match.group(8)}', '%H:%M:%S.%f')
            
#             # Adjust timestamps by adding the offset
#             start_time += offset
#             end_time += offset
            
#             # Format the timestamps back to SRT format
#             start_time_str = start_time.strftime('%H:%M:%S,%f')[:-3]
#             end_time_str = end_time.strftime('%H:%M:%S,%f')[:-3]
            
#             adjusted_line = f"{start_time_str} --> {end_time_str}"
#             adjusted_srt.append(adjusted_line)
#         else:
#             adjusted_srt.append(line)
    
#     return adjusted_srt

# # Function to read and stitch multiple SRT files
# def stitch_srt_files(files):
#     final_srt = []
#     total_offset = timedelta(seconds=0)

#     for i, file in enumerate(files):
#         with open(file, 'r') as f:
#             srt_lines = f.readlines()

#         # Adjust timestamps for each SRT file based on the total offset
#         adjusted_srt = adjust_timestamp(srt_lines, total_offset)
#         final_srt.extend(adjusted_srt)
        
#         # Update the offset to reflect the start of the next interval
#         if i < len(files) - 1:
#             total_offset += timedelta(seconds=30 * 60)  # Add 30 minutes for the next interval

#     # Save the final combined SRT file
#     with open('final_output.srt', 'w') as f:
#         f.writelines(final_srt)

# # List of SRT files to stitch
# srt_files = ['srt_1.srt', 'srt_2.srt', 'srt_3.srt', 'srt_4.srt', 'srt_5.srt', 'srt_6.srt', 'srt_7.srt']

# stitch_srt_files(srt_files)


import os
import re

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

def adjust_timestamps_and_stitch(segments_list):
    """Adjust timestamps to create a continuous flow and combine all segments."""
    combined_segments = []
    current_end_time = "00:00:00,000"  # Start at 00:00:00,000
    
    for segments in segments_list:
        for segment in segments:
            start_time = segment["start_time"]
            end_time = segment["end_time"]
            text = segment["text"]
            
            # Update the start time to match the previous segment's end time
            if start_time != "00:00:00,000" and start_time != current_end_time:
                start_time = current_end_time

            # Update the end time to the current segment's end time
            current_end_time = end_time

            combined_segments.append({
                "start_time": start_time,
                "end_time": end_time,
                "text": text
            })
    
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

