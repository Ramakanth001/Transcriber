from moviepy.video.io.VideoFileClip import VideoFileClip
import ffmpeg

def split_and_compress_video(input_file, start_time, end_time, output_file):
    try:
        # Load the video
        with VideoFileClip(input_file) as video:
            # Create a subclip based on the start and end times
            subclip = video.subclip(start_time, end_time)

            # Write the output file with a specific codec and bitrate for compression
            subclip.write_videofile(output_file,
                                    codec="libx264",  # H.264 codec for compression
                                    preset="ultrafast",  # You can adjust this to control speed/compression
                                    bitrate="1500k",  # Set target bitrate for compression (lower = smaller size)
                                    audio_codec="aac",  # Audio codec
                                    threads=4)  # Set threads for faster processing
    except Exception as e:
        print(f"An error occurred: {e}")  
            

def timestamp_video_split(input_video, start_time, end_time, output_video):
    try:
        # Load the video
        video = VideoFileClip(input_video)

        # Extract the subclip
        subclip = video.subclip(start_time, end_time)

        # Write the subclip to a new file with the original codecs, no extra compression
        subclip.write_videofile(
            output_video,                            
            codec='copy',         
             # Copy original video codec
                                
            audio_codec='copy',   
            # Copy original audio codec
                                
            threads=4)
            # Enable multi-threading
                                
        # codec='rawvideo' (Lossless, uncompressed video) and audio_codec='pcm_s16le',  # Uncompressed audio
        # codec='libx264', audio_codec='aac', preset="ultrafast") - this is faster 
        print(f"Video split successfully! Saved as {output_video}")

    except Exception as e:
        print(f"Error: {e}")






