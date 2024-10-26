from moviepy.video.io.VideoFileClip import VideoFileClip
import torch
from pydub import AudioSegment

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds * 1000) % 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_video_duration(video_file):
    try:
        video = VideoFileClip(video_file)

        # This gives the duration in seconds
        duration = video.duration  
        video.close()
        
        # Converts the video into HSM format
        hsm_format_duration = format_duration(duration)

        return hsm_format_duration 

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_audio_duration(audio_file):
    """Get the duration of the audio in seconds."""
    audio = AudioSegment.from_file(audio_file)
    return len(audio) / 1000  # Convert from milliseconds to seconds

def check_gpu():
    print("CUDA Available: ", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU Name: ", torch.cuda.get_device_name(0))
        print("Memory Allocated: ", torch.cuda.memory_allocated(0)/1024**3, "GB")
        print("Total Memory: ", torch.cuda.get_device_properties(0).total_memory/1024**3, "GB")
