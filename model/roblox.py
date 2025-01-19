import processors.audio_processor as audio_processor
import processors.common as common
import processors.srt_processor as srt_processor
import processors.srt_sticher as srt_sticher
import os
import shutil

def video_to_audio(input_video, output_audio_name):
    start_time = input("Enter start time (HH:MM:SS): \n'Hit ENTER button if you want to process from the beginning\n")

    if not start_time:
        start_time = "00:00:00"
    end_time = input("Enter end time (HH:MM:SS): \n'Hit ENTER button if you want to process till the end\n")

    if not end_time:
        end_time = common.get_video_duration(input_video)   

    audio_processor.extract_hd_audio_from_video(input_video, output_audio_name, start_time, end_time)
    print("Audio file saved as:", output_audio_name)

def split_audio(audio_file, frequency):
    output_folder = f"{audio_file.split('.')[0]}_output_audio_segment_files"
    audio_duration = common.get_audio_duration(audio_file)
    print(audio_duration), type(audio_duration)
    timestamps = audio_processor.timestamp_splitter(frequency,audio_duration)
    print("timestamps for reference:\n",timestamps)
    audio_processor.split_audio_based_on_timestamps_ffmpeg(audio_file, timestamps, output_folder)
    print("Segmented audio files are stored in the following folder:\n",output_folder)
    return output_folder

def get_audio_files_in_folder(folder_path):
    # Get all m4a files in the folder
    return [f for f in os.listdir(folder_path) if f.endswith('.m4a')]

def process_all_audio_files_to_srt(folder_path, model_size="medium"):
    audio_files = get_audio_files_in_folder(folder_path)
    srt_folder_path = f"{folder_path}_srt"

    # Create the SRT folder if it doesn't exist
    if not os.path.exists(srt_folder_path):
        os.makedirs(srt_folder_path)
        print(f"Created folder: {srt_folder_path}")
    
    for audio_file in audio_files:
        input_audio_file = os.path.join(folder_path, audio_file)
        output_srt_file = os.path.join(srt_folder_path, f"{os.path.splitext(audio_file)[0]}.srt")
        
        print(f"Processing audio file: {audio_file}")
        
        # Call your transcribe function here and specify the output path
        srt_processor.transcribe_audio_with_srt(input_audio_file)

        # Build the expected SRT file path based on input audio file
        original_srt_file = os.path.splitext(input_audio_file)[0] + f"_{model_size}.srt"

        # Debugging: Check if the file exists after transcription
        print(f"Looking for SRT file at: {original_srt_file}")

        # If the SRT file exists, move it to the SRT folder
        if os.path.exists(original_srt_file):
            new_srt_file = os.path.join(srt_folder_path, os.path.basename(original_srt_file))
            shutil.move(original_srt_file, new_srt_file)  # Move the file
            print(f"Moved SRT file for {audio_file} to {new_srt_file}")
        else:
            print(f"Warning: SRT file for {audio_file} not found at expected location: {original_srt_file}")

    print(f"All SRT files have been saved in the '{srt_folder_path}' folder.")
    return srt_folder_path


# def process_all_audio_files_to_srt(folder_path):
#     audio_files = get_audio_files_in_folder(folder_path)
#     srt_folder_path = f"{folder_path}_srt"

#     if not os.path.exists(srt_folder_path):
#         os.makedirs(srt_folder_path)
#         print(f"Created folder: {srt_folder_path}")
    
#     for audio_file in audio_files:
#         input_audio_file = os.path.join(folder_path, audio_file)
#         output_srt_file = os.path.join(srt_folder_path, f"{os.path.splitext(audio_file)[0]}.srt")
        
#         # Call your transcribe function here
#         srt_processor.transcribe_audio_with_srt(input_audio_file)

#         original_srt_file = os.path.splitext(input_audio_file)[0] + ".srt"

#         # If the file is saved in the default location, move it to the SRT folder
#         if os.path.exists(original_srt_file):
#             new_srt_file = os.path.join(srt_folder_path, os.path.basename(original_srt_file))
#             shutil.move(original_srt_file, new_srt_file)  # Move the file
#             print(f"Moved SRT file for {audio_file} to {new_srt_file}")
#         else:
#             print(f"Warning: SRT file for {audio_file} not found in the default location.")

#     print(f"All SRT files have been saved in the '{srt_folder_path}' folder.")
#     return srt_folder_path

def roblox_driver():
    
    print("sample path --> /mnt/e/projects/Krishna.mp4")
    input_video = input("Give the video path:\n")
    input_video = "/mnt/e/projects/Krishna.mp4"

    print("\nsample output audio --> Swami_DJ_audio.m4a")
    output_audio_name = input("Enter output audio file name:\n")
    output_audio_name = "Swami_DJ_audio.m4a"

    video_to_audio(input_video, output_audio_name)

    frequency = int(input("\nEnter Frequency in minutes to split the audio file into segemnts:\n"))
    audios_folder = split_audio(output_audio_name, frequency)

    srt_folder_path = process_all_audio_files_to_srt(audios_folder)

    combined_srt_file = "DattaJayanti_combined_srt_file.srt"
    srt_sticher.stitch_srt_files(srt_folder_path, combined_srt_file)
    print(f"SRT files have been combined into {combined_srt_file}")

    print("All audio files processed successfully.")

    raw_srt_file = srt_processor.srt_to_raw_transcript(combined_srt_file)
    print("Transcript file is at:", raw_srt_file)

def resumed():
    # srt_folder_path = "Gurupurnima_audio_output_audio_segment_files_srt"
    combined_srt_file = "DattaJayanti_combined_srt_file.srt"

    srt_folder_path = "Swami_DJ_audio_output_audio_segment_files_srt"

    combined_srt_file = "DattaJayanti_combined_srt_file.srt"
    srt_sticher.stitch_srt_files(srt_folder_path, combined_srt_file)
    print(f"SRT files have been combined into {combined_srt_file}")

    print("All audio files processed successfully.")

    raw_srt_file = srt_processor.srt_to_raw_transcript(combined_srt_file)
    print("Transcript file is at:", raw_srt_file)

if __name__ == "__main__":
    # resumed()
    roblox_driver()