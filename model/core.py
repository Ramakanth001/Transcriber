import processors.common as common
import processors.video_processor as video_processor
import processors.srt_processor as srt_processor
import processors.audio_processor as audio_processor
import fine_tuning.data_set_generator as data_set_generator
import fine_tuning.fine_tune as fine_tuner

# import fine_tuning.fine_tune as fine_tune

def driver_code():
    print("****************************************************************")

    main_choice = int(input("Choose one of the following:\n1. Split the video\n2. Split audio\n3. Convert video to audio\n4. Convert audio to SRT and RAW files\n5. Generate Dummy SRT file as per audio\n6. Fine tune the model with custom audio and SRT\n"))

    if main_choice == 1 :

        compression_flag = input("Do you want to compress the video? (y/n):\n")
        
        input_video = input("Give the video path:\n")

        #hard coded for testing
        input_video = "/mnt/e/projects/Krishna.mkv"

        # If start time is not specified then then zeroth second will be considered as the start time by default
        start_time = input("Enter start time (HH:MM:SS): \n'Hit ENTER button if you want to process from the beginning\n")

        if not start_time:
            start_time = "00:00:00"

        # If end time is not specified then the total duration will be considered as the end time by default
        end_time = input("Enter end time (HH:MM:SS): \n'Hit ENTER button if you want to process till the end\n")

        if not end_time:
            end_time = common.get_video_duration(input_video)

        output_video = input("Enter output video file name:\n")
        
        # hard-coded Output video file name
        output_video = "Swami_video_1_3.mp4"

        if(compression_flag.lower() == "y"):
            print("Splitting and Compressing the video...")
            video_processor.split_and_compress_video(input_video, start_time, end_time, output_video)
        
        if(compression_flag.lower() == "n"):
            print("Splitting the video")
            video_processor.timestamp_video_split(input_video, start_time, end_time, output_video)

    if main_choice == 2 :    
        # Example usage:
        audio_file = "/mnt/e/projects/TG-1_Full.wav"
        timestamps = [(0, 300), (300, 600), (600, 1200), (1200, 1800), (1800, 2271) ]  
        # Example timestamps in seconds
        output_folder = "output_segments"
        audio_processor.split_audio(audio_file, timestamps, output_folder)


    if main_choice == 3:

        input_video = input("Give the video path:\n")

        #hard coded for testing
        input_video = "/mnt/e/projects/Krishna.mkv"

        # If start time is not specified then then zeroth second will be considered as the start time by default
        start_time = input("Enter start time (HH:MM:SS): \n'Hit ENTER button if you want to process from the beginning\n")

        if not start_time:
            start_time = "00:00:00"

        # If end time is not specified then the total duration will be considered as the end time by default
        end_time = input("Enter end time (HH:MM:SS): \n'Hit ENTER button if you want to process till the end\n")

        if not end_time:
            end_time = common.get_video_duration(input_video)
            
        output_audio = input("Enter output audio file name:\n")

        if not output_audio:

            # hard-coded Output video file name
            output_audio = "Swami_audio_1_3.m4a"

        audio_processor.extract_hd_audio(input_video, output_audio, start_time, end_time)


    if main_choice == 4:

        input_audio = input("Give the audio file path:\n")

        #hard coded for testing
        input_audio = "files/sample_3/Swami_audio_sample_3_1-10-00_1-23-25.m4a"
    
        srt_file = srt_processor.transcribe_audio_with_srt(input_audio)
        print(srt_file)

        raw_srt_file = srt_processor.srt_to_raw_transcript(srt_file)
        print(raw_srt_file)

    if main_choice == 5:

        audio_file_path = input("\nGive the audio file path:\n")

        #hard coded for testing
        audio_file_path = "training_data/TG-1/segment_1.wav"

        segment_duration = input("Enter segment duration in seconds:\n(Hit enter for default segment duration - 10 seconds)\n")

        if not segment_duration:
            segment_duration = 10

        srt_processor.generate_dummy_srt(audio_file_path, segment_duration)

    if main_choice == 6:

        audio_file_path = input("\nGive the audio file path:\n")
        
        # Paths to the audio file and its corresponding SRT file
        audio_file_path = "training_data/TG-1/segment_1.wav"

        srt_file_path = input("\nGive the SRT file path:\n")
        srt_file_path = "training_data/TG-1/segment_1.srt"

        # Prepare datasets with a random 80-20 train-validation split
        train_dataset, val_dataset = data_set_generator.prepare_data_with_single_file(audio_file_path, srt_file_path, test_size=0.2)

        fine_tuned_model_dir = fine_tuner(train_dataset, val_dataset, output_dir="fine_tuned_model")

        print(f"Fine-tuned model saved at: {fine_tuned_model_dir}")


if __name__ == "__main__":
    driver_code()
    # fine_tune.fine_tune_model()


    # TODO:
    # 3. Language wide parameters
    # 4. If video is given directlt srt and raw should comw
    # 5. Timestamp for audio to srt conversion feature
    # 6. Audio splitting feature

    # GOAL:
    # AI Model -> Question - relevant answer - generate speech - generate video (advanced work)