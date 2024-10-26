from sklearn.model_selection import train_test_split
import os

def prepare_data_with_split(folder_path, test_size=0.2):
    # Get all .wav and .srt files in the folder
    audio_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".wav")])
    srt_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".srt")])

    # Ensure that both lists match by file name (without extension)
    audio_basenames = [os.path.splitext(os.path.basename(f))[0] for f in audio_files]
    srt_basenames = [os.path.splitext(os.path.basename(f))[0] for f in srt_files]

    # Match audio files with corresponding SRT files
    matched_audio_files = []
    matched_srt_files = []

    for i, basename in enumerate(audio_basenames):
        if basename in srt_basenames:
            matched_audio_files.append(audio_files[i])
            matched_srt_files.append(srt_files[srt_basenames.index(basename)])

    # Split into training and validation sets
    train_audio_files, val_audio_files, train_srt_files, val_srt_files = train_test_split(
        matched_audio_files, matched_srt_files, test_size=test_size, random_state=42
    )

    # Create datasets for training and validation
    train_data = {"audio": train_audio_files, "transcription": train_srt_files}
    val_data = {"audio": val_audio_files, "transcription": val_srt_files}

    train_dataset = load_dataset('csv', data_files=train_data)
    val_dataset = load_dataset('csv', data_files=val_data)

    # Cast the `audio` column to a format suitable for the model
    train_dataset = train_dataset.cast_column("audio", Audio(sampling_rate=16000))
    val_dataset = val_dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Map the transcription into a format the model expects (using processor.tokenizer)
    train_dataset = train_dataset.map(lambda batch: processor(batch["transcription"]), batched=True)
    val_dataset = val_dataset.map(lambda batch: processor(batch["transcription"]), batched=True)

    return train_dataset, val_dataset
