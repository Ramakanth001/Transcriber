

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

