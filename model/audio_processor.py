

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