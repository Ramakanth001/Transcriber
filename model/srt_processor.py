
def transcribe_audio_with_srt(audio_file):

    # Load the Whisper model 
    model = whisper.load_model("medium") 
    
    result = model.transcribe(audio_file)
    
    # Create the SRT file
    srt_file = os.path.splitext(audio_file)[0] + ".srt"
    
    with open(srt_file, "w") as srt:
        for idx, segment in enumerate(result['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            # Format timestamps to SRT style (HH:MM:SS,MSS)
            start_time = format_duration(start)
            end_time = format_duration(end)
            
            # Write to SRT file
            srt.write(f"{idx + 1}\n")
            srt.write(f"{start_time} --> {end_time}\n")
            srt.write(f"{text}\n\n")

    return srt_file