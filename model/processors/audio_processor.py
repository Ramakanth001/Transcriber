import moviepy.editor as mp
import ffmpeg
import concurrent.futures
import os

def extract_hd_audio_from_video(input_video, output_audio, start_time, end_time):
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


def timestamp_splitter(frequency,duration):
    # duration = '05:51:14'  # Example duration in HH:MM:SS
    print(frequency)
    hours = int(duration[:2])  # Extract hours from the duration
    minutes = int(duration[3:5])  # Extract minutes from the duration
    seconds = int(duration[6:])  # Extract seconds from the duration
    
    # Calculate the total number of minutes in the duration
    total_minutes = hours * 60 + minutes

    # Calculate the number of full frequency segments
    number_of_segments = total_minutes // frequency  # Base number of full segments
    if total_minutes % frequency != 0:
        number_of_segments += 1  # Add an extra segment if there's a remainder

    # Initialize the timestamp array and starting time
    timestamp_array = []
    current_hour = 0
    current_minute = 0
    current_second = 0
    
    # Add the first timestamp, starting at 00:00:00
    timestamp_array.append(f"{current_hour:02}:{current_minute:02}:{current_second:02}")
    
    # Generate timestamps for the full frequency segments
    for i in range(1, number_of_segments):
        # Calculate the next timestamp based on frequency
        current_minute = (i * frequency) % 60
        current_hour = (i * frequency) // 60
        timestamp_array.append(f"{current_hour:02}:{current_minute:02}:{current_second:02}")
    
    # Handling the last timestamp based on the remaining duration
    # The last timestamp should reflect the exact end time, which is duration - last frequency
    last_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}"
    timestamp_array.append(last_timestamp)

    print(f"Final Timestamp Array: {timestamp_array}")
    return timestamp_array


def split_audio_based_on_timestamps_ffmpeg(input_audio_file, timestamps, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i in range(1, len(timestamps)):
        start_time = timestamps[i-1]
        end_time = timestamps[i]
        
        # Output file name
        output_file = os.path.join(output_folder, f"audio_segment_{i}.m4a")
        
        # Use ffmpeg to extract the segment with the highest quality settings
        ffmpeg.input(input_audio_file, ss=start_time, to=end_time).output(output_file, acodec='aac', audio_bitrate='320k', format='ipod').run()

        print(f"Segment {i} saved as {output_file}")


# We are not using this function using mp
def split_audio_using_moviepy(audio_file, timestamps, output_folder):
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