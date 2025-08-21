import os
import wave
import whisper
from .common import get_audio_duration
from datetime import timedelta

# Load the Whisper model 
model_size="medium"
# model_size="large"

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)  # Extract milliseconds
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"  # Correct SRT format

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

# Refactored approach
import os
import whisper
from pydub import AudioSegment
import torch
import json

model_size = "medium"  # safe for GTX 1650 (4GB VRAM)

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def load_model_safe(size):
    """Load Whisper model with CUDA if available, else fallback to CPU"""
    if torch.cuda.is_available():
        try:
            return whisper.load_model(size).to("cuda")
        except RuntimeError:
            print("⚠️ CUDA OOM, switching to CPU...")
            return whisper.load_model(size).to("cpu")
    else:
        print("CUDA not available, running on CPU")
        return whisper.load_model(size).to("cpu")

def transcribe_audio_with_chunks(audio_file, chunk_length=600):  # 600s = 10 mins
    # Load model once
    model = load_model_safe(model_size)

    # Load audio and get duration
    audio = AudioSegment.from_file(audio_file)
    duration = len(audio) / 1000  # in seconds
    print(f"Audio duration: {duration/3600:.2f} hours")

    # Output SRT + progress file
    srt_file = os.path.splitext(audio_file)[0] + f"_{model_size}_merged.srt"
    progress_file = srt_file + ".progress"

    # Figure out resume state
    start_chunk = 0
    index = 1
    offset = 0.0
    if os.path.exists(progress_file):
        with open(progress_file, "r") as pf:
            progress = json.load(pf)
            start_chunk = progress.get("last_chunk", 0) + 1
            index = progress.get("last_index", 1)
            offset = progress.get("last_offset", 0.0)
        print(f"Resuming from chunk {start_chunk}, index {index}, offset {offset:.2f}s")

    # If fresh start, clear file
    if start_chunk == 0:
        open(srt_file, "w", encoding="utf-8").close()

    # Process chunks
    for i in range(start_chunk * chunk_length * 1000, len(audio), chunk_length * 1000):
        chunk_num = i // (chunk_length * 1000)
        chunk = audio[i:i + chunk_length * 1000]
        chunk_file = f"temp_chunk_{chunk_num}.wav"
        chunk.export(chunk_file, format="wav")

        print(f"Processing chunk {chunk_num}: {chunk_file} (offset={offset:.2f}s)")

        # Transcribe chunk
        result = model.transcribe(
            chunk_file,
            language="en",
            fp16=False,
            condition_on_previous_text=False,
            temperature=0
        )

        with open(srt_file, "a", encoding="utf-8") as srt:
            for seg in result["segments"]:
                start = seg["start"] + offset
                end = seg["end"] + offset
                text = seg["text"].strip()

                srt.write(f"{index}\n")
                srt.write(f"{format_duration(start)} --> {format_duration(end)}\n")
                srt.write(f"{text}\n\n")
                index += 1

        # Update offset
        offset += chunk.duration_seconds

        # Save progress
        with open(progress_file, "w") as pf:
            json.dump({"last_chunk": chunk_num, "last_index": index, "last_offset": offset}, pf)

    print(f"SRT saved: {srt_file}")
    print("✅ All chunks processed. You can delete the .progress file if not needed.")
    return srt_file

