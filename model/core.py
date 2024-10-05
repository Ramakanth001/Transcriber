

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

        output_audio = input("Enter output audio file name:\n")

        if not output_audio:

            # hard-coded Output video file name
            output_audio = "Swami_audio_1_3.m4a"

        extract_hd_audio(input_video, output_audio, start_time, end_time)

if __name__ == "__main__":
    # driver_code()
    audio_file = "Swami_audio_1_3.m4a"
    srt_file = transcribe_audio_with_srt(audio_file)

    # TODO:
    # 1. Enable GPU processing
    # 2. Language wide parameters
    # GOAL:
    # AI Model -> Question - relevant answer - generate speech - generate video (advanced work)