from transformers import WhisperForConditionalGeneration, WhisperProcessor, Seq2SeqTrainer, Seq2SeqTrainingArguments
import data_set_generator

#The below is Supervised learning model

def fine_tune_model(train_dataset, val_dataset, output_dir="fine_tuned_model"):
    # Load a pre-trained Whisper model and processor
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").to("cuda")
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")

    # Set up training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,             # Directory to store model checkpoints
        # per_device_train_batch_size=2,     # Adjust based on your GPU capacity
        per_device_train_batch_size=1,     # Adjust based on your GPU capacity
        per_device_eval_batch_size=2,
        num_train_epochs=3,                # Number of epochs
        fp16=True,                         # Use mixed precision (reduce memory)
        save_steps=500,                    # Save checkpoint every 500 steps
        evaluation_strategy="steps",       # Evaluate every few steps
        eval_steps=500,
        save_total_limit=2,                # Only keep the last 2 checkpoints
        learning_rate=5e-5,
        logging_dir=f"{output_dir}/logs"
    )

    # Create trainer instance
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=processor.tokenizer,
    )

    # Fine-tune the model
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model(output_dir)
    processor.save_pretrained(output_dir)

    return output_dir


# Path to the folder containing all the audio and SRT files
folder_path = "path/to/your/folder"

# Prepare datasets with a random 80-20 train-validation split
train_dataset, val_dataset = data_set_generator.prepare_data_with_split(folder_path, test_size=0.2)
