from .common import format_duration
import whisper
import os

def transcribe_audio_with_srt(audio_file):

    # Load the Whisper model 
    model = whisper.load_model("medium").to("cuda")
    
    result = model.transcribe(audio_file, language="en")

    # result = model.transcribe(audio_file, language="en", word_timestamps=False, verbose=False)

    
    # Create the SRT file
    srt_file = os.path.splitext(audio_file)[0] + ".srt"
    
    with open(srt_file, "w") as srt:
        for idx, segment in enumerate(result['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            # Format timestamps to SRT style (HH:MM:SS,MSS)
            start_time = format_duration(start)
            end_time = format_duration(end)
            
            # Write to SRT file
            srt.write(f"{idx + 1}\n")
            srt.write(f"{start_time} --> {end_time}\n")
            srt.write(f"{text}\n\n")

    return srt_file


def srt_to_raw_transcript(srt_file_path):
    # Determine the output file path
    base_name = os.path.splitext(srt_file_path)[0]  # Get the base name without extension
    output_file_path = f"{base_name}_raw_transcript.txt"  # Append '_raw_transcript' to the base name

    with open(srt_file_path, 'r') as srt_file:
        lines = srt_file.readlines()

    # Prepare to collect the transcript lines
    transcript_lines = []

    for line in lines:
        # Remove line numbers and timestamps
        if line.strip().isdigit() or "-->" in line or line.strip() == "":
            continue  # Skip numbers, timestamps, and empty lines
        transcript_lines.append(line.strip())  # Add the text line

    # Write the transcript to the output file
    with open(output_file_path, 'w') as output_file:
        for transcript_line in transcript_lines:
            output_file.write(transcript_line + "\n")

    print(f"Transcript saved to: {output_file_path}")  # Print confirmation message
