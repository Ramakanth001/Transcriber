from transformers import WhisperForConditionalGeneration, WhisperProcessor, Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq

def fine_tune_model(train_dataset, val_dataset, output_dir="fine_tuned_model"):
    # Load a pre-trained Whisper model and processor
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium").to("cuda")
    processor = WhisperProcessor.from_pretrained("openai/whisper-medium")

    # Prepare data collator for dynamic padding
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=processor.tokenizer,
        model=model,
        padding=True,
        return_tensors="pt"
    )

    # Set up training arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,             # Directory to store model checkpoints
        per_device_train_batch_size=1,     # Adjust based on your GPU capacity
        per_device_eval_batch_size=2,
        num_train_epochs=3,                # Number of epochs
        fp16=True,                         # Use mixed precision (reduce memory)
        save_steps=500,                    # Save checkpoint every 500 steps
        evaluation_strategy="steps",       # Evaluate every few steps
        eval_steps=500,
        save_total_limit=2,                # Only keep the last 2 checkpoints
        learning_rate=5e-5,
        logging_dir=f"{output_dir}/logs",
        report_to="tensorboard"            # Log training progress to TensorBoard
    )

    # Create trainer instance
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=processor.tokenizer,
        data_collator=data_collator
    )

    # Fine-tune the model
    trainer.train()

    # Save the fine-tuned model and processor
    trainer.save_model(output_dir)
    processor.save_pretrained(output_dir)

    return output_dir
