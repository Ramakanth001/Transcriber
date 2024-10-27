from sklearn.model_selection import train_test_split
import os
import pandas as pd
from datasets import Dataset, Audio
from transformers import WhisperProcessor, DataCollatorForSeq2Seq, Seq2SeqTrainer

# Initialize the processor globally
processor = WhisperProcessor.from_pretrained("openai/whisper-medium")

def prepare_data_with_single_file(audio_file, srt_file, test_size=0.2):
    # Ensure both the audio file and SRT file exist
    if not os.path.exists(audio_file) or not os.path.exists(srt_file):
        raise FileNotFoundError("Audio file or SRT file not found.")

    # Read the transcription from the SRT file
    with open(srt_file, 'r', encoding='utf-8') as f:
        transcription_text = f.read()

    # Create a dictionary containing the audio file path and its transcription
    data = {"audio": [audio_file], "transcription": [transcription_text]}
    
    # Create a pandas DataFrame
    df = pd.DataFrame(data)

    # Split the data into training and validation sets manually, since we have a single example
    if len(df) == 1:
        train_df = df
        val_df = pd.DataFrame(columns=df.columns)  # Empty validation DataFrame
    else:
        train_df, val_df = train_test_split(df, test_size=test_size, random_state=42)

    # Convert DataFrames to HuggingFace datasets
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)

    # Cast the `audio` column to a format suitable for the model
    train_dataset = train_dataset.cast_column("audio", Audio(sampling_rate=16000))
    if len(val_df) > 0:
        val_dataset = val_dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Define the preprocess function before mapping
    def preprocess_function(batch):
        # Process the transcription into model inputs with padding and truncation
        result = processor(
            text=batch["transcription"],
            padding=True,            # Pads to the longest sequence in the batch by default
            truncation=True,         # Truncates if input is longer than max_length
            max_length=448,          # Adjust max_length based on model and GPU capacity
            return_tensors="pt"      # Use PyTorch tensors for compatibility
        )
        # Return only the input_ids and attention_mask fields with consistent lengths
        return {
            "input_ids": result["input_ids"][0], 
            "attention_mask": result["attention_mask"][0]
        }

    # Apply the mapping with the preprocess function
    train_dataset = train_dataset.map(preprocess_function, batched=True, remove_columns=["transcription"])
    if len(val_df) > 0:
        val_dataset = val_dataset.map(preprocess_function, batched=True, remove_columns=["transcription"])

    return train_dataset, val_dataset