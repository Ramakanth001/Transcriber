import moviepy.editor as mp
import concurrent.futures
import os

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
                                            ffmpeg_params=["-ar", "44100"])  
                # No need for bitrate since WAV is uncompressed
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
        future.result()  
        # Wait for the extraction to complete

def split_audio(audio_file, timestamps, output_folder):
    """
    Splits an audio file based on given timestamps using moviepy.
    
    Parameters:
    - audio_file (str): Path to the audio file (e.g., "input_audio.wav").
    - timestamps (list of tuples): List of (start, end) tuples where each timestamp is in seconds.
    - output_folder (str): Path to the folder where the split files will be saved.
    
    Example:
    timestamps = [(0, 60), (120, 180)]  # Split from 0s to 60s and 120s to 180s
    """
    # Load the audio file using moviepy
    audio = mp.AudioFileClip(audio_file)
    
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over the timestamps and split the audio
    for i, (start_time, end_time) in enumerate(timestamps):
        # Extract the segment using subclip
        segment = audio.subclip(start_time, end_time)

        # Define the output file name
        output_file = os.path.join(output_folder, f"segment_{i + 1}.wav")

        # Write the audio segment to the output file
        segment.write_audiofile(output_file, codec='pcm_s16le')
        print(f"Segment {i + 1} saved as {output_file}")

    # Close the audio clip to free resources
    audio.close()

