from moviepy.video.io.VideoFileClip import VideoFileClip
import ffmpeg
import moviepy.editor as mp
import concurrent.futures

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
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

def extract_hd_audio(input_video, output_audio, start_time, end_time):
    # Function to extract audio
    def audio_extraction():
        try:
            # Load only the required subclip of the video
            video = mp.VideoFileClip(input_video).subclip(start_time, end_time)

            # Subclip the audio to the same duration
            audio_clip = video.audio

            # Write audio to a file with high quality settings
            if output_audio.endswith('.m4a'):
                audio_clip.write_audiofile(output_audio, codec='aac', 
                                            ffmpeg_params=["-b:a", "320k", "-ar", "44100"])
            elif output_audio.endswith('.wav'):
                audio_clip.write_audiofile(output_audio, codec='pcm_s16le', 
                                            ffmpeg_params=["-ar", "44100"])  # No need for bitrate since WAV is uncompressed
            else:
                raise ValueError("Unsupported file extension. Use .m4a or .wav.")

            print(f"Audio extracted successfully to: {output_audio}")

        except Exception as e:
            print(f"Error during audio extraction: {e}")
        finally:
            # Close the clips to release resources
            if 'audio_clip' in locals():
                audio_clip.close()
            if 'video' in locals():
                video.close()

    # Use a thread pool to run the audio extraction
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(audio_extraction)
        future.result()  # Wait for the extraction to complete

def driver_code():
    print("****************************************************************")

    main_choice = int(input("Choose one of the following:\n1. Split the video\n2. Convert video to audio\n"))

    if main_choice == 1 :

        compression_flag = input("Do you want to compress the video? (y/n):\n")
        
        input_video = input("Give the video path:\n")

        #hard coded for testing
        input_video = "/mnt/c/Users/Ramakanth/Downloads/Krishna.mkv"

        # If start time is not specified then then zeroth second will be considered as the start time by default
        start_time = input("Enter start time (HH:MM:SS): \n'Hit ENTER button if you want to process from the beginning\n")

        # If end time is not specified then the total duration will be considered as the end time by default
        end_time = input("Enter end time (HH:MM:SS): \n'Hit ENTER button if you want to process till the end\n")

        output_video = input("Enter output video file name:\n")
        
        # hard-coded Output video file name
        output_video = "Swami_video_1_3.mp4"

        if(compression_flag.lower() == "y"):
            print("Splitting and Compressing the video...")
            split_and_compress_video(input_video, start_time, end_time, output_video)
        
        if(compression_flag.lower() == "n"):
            print("Splitting the video")
            timestamp_video_split(input_video, start_time, end_time, output_video)

    if main_choice == 2:

        input_video = input("Give the video path:\n")

        #hard coded for testing
        input_video = "/mnt/c/Users/Ramakanth/Downloads/Krishna.mkv"

        # If start time is not specified then then zeroth second will be considered as the start time by default
        start_time = input("Enter start time (HH:MM:SS): \n'Hit ENTER button if you want to process from the beginning\n")

        # If end time is not specified then the total duration will be considered as the end time by default
        end_time = input("Enter end time (HH:MM:SS): \n'Hit ENTER button if you want to process till the end\n")

        output_audio = input("Enter output video file name:\n")
        
        # hard-coded Output video file name
        output_audio = "Swami_audio_1_3.m4a"

        extract_hd_audio(input_video, output_audio, start_time, end_time)

if __name__ == "__main__":
    driver_code()