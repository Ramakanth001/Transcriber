import os
import wave
import whisper
from .common import format_duration
from .common import get_audio_duration
from datetime import timedelta

# Load the Whisper model 
model_size="medium"
# model_size="large"


def transcribe_audio_with_srt(audio_file):

    model = whisper.load_model(model_size).to("cuda")
    # model = whisper.load_model("large").to("cuda")
    
    result = model.transcribe(audio_file, language="en")

    # result = model.transcribe(audio_file, language="en", word_timestamps=False, verbose=False)

    
    # Create the SRT file
    srt_file = os.path.splitext(audio_file)[0] + "_" + model_size + ".srt"
    
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
    output_file_path = f"{base_name}_transcript.txt"  # Append '_transcript' to the base name

    with open(srt_file_path, 'r') as srt_file:
        lines = srt_file.readlines()

    # Prepare to collect the transcript lines
    transcript_text = []  # Store lines to join later

    for line in lines:
        # Remove line numbers and timestamps
        if line.strip().isdigit() or "-->" in line or line.strip() == "":
            continue  # Skip numbers, timestamps, and empty lines
        transcript_text.append(line.strip())  # Add the text line

    # Join lines with a period and a space
    transcript_output = ". ".join(transcript_text) + "."  # Add final period at end

    # Write the transcript to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(transcript_output)

    print(f"Transcript saved to: {output_file_path}")  # Print confirmation message


def convert_transcript_to_srt(audio_file, transcript_file, segment_duration):
    # Get audio duration
    audio_duration = get_audio_duration(audio_file)

    # Read the transcript from the .txt file
    with open(transcript_file, 'r') as file:
        lines = file.readlines()

    # Generate the output SRT file path with the new naming convention
    base_name = os.path.splitext(transcript_file)[0]
    srt_file = f"{base_name}_SRT_converted.srt"

    # Prepare the SRT content
    srt_content = []
    start_time = 0

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        end_time = start_time + segment_duration
        # Ensure we don't exceed the audio duration
        if end_time > audio_duration:
            end_time = audio_duration

        # Format timestamps to SRT style (HH:MM:SS,MSS)
        start_srt = format_duration(start_time)
        end_srt = format_duration(end_time)

        # Create the SRT entry
        srt_content.append(f"{idx + 1}\n{start_srt} --> {end_srt}\n{line}\n")
        
        # Update the start time for the next line
        start_time = end_time

        if end_time >= audio_duration:  # Stop if we reach the audio duration
            break

    # Write the SRT content to a file
    with open(srt_file, 'w') as file:
        file.writelines(srt_content)

    print(f"SRT file created at: {srt_file}")



def get_audio_duration(audio_file):
    """Get the duration of an audio file in seconds."""
    with wave.open(audio_file, 'rb') as audio:
        frames = audio.getnframes()
        rate = audio.getframerate()
        duration = frames / float(rate)
    return duration


def generate_dummy_srt(audio_file, segment_duration):

    """Generate a dummy SRT file for an audio file based on the segment duration."""

    srt_output_path = f"{os.path.splitext(audio_file)[0]}_dummy.srt"


    # Get audio duration
    duration = get_audio_duration(audio_file)
    
    # Calculate the number of segments
    segments = int(duration // segment_duration) + (1 if duration % segment_duration > 0 else 0)
    
    # Prepare SRT content
    srt_content = []
    for i in range(segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, duration)
        
        start_srt = format_duration(start_time)
        end_srt = format_duration(end_time)
        
        # Create the SRT entry
        srt_content.append(f"{i + 1}\n{start_srt} --> {end_srt}\ntext\n\n")
    
    # Write to the SRT file
    with open(srt_output_path, 'w', encoding='utf-8') as file:
        file.writelines(srt_content)
    
    print(f"SRT file generated at: {srt_output_path}")

#test01
