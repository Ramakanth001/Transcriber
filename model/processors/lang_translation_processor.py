import srt
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from indicnlp.normalize.indic_normalize import IndicNormalizer

def load_model_and_tokenizer():
    """Load IndicTrans2 model and tokenizer."""
    model_name = "ai4bharat/indictrans2-en-indic-dist-200M"  # Use "1B" for larger model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return model, tokenizer

def translate_text(model, tokenizer, text, target_lang="hi"):
    """Translate English text to target Indic language."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model.generate(**inputs, max_length=512, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang])
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def normalize_indic_text(text, lang_code):
    """Normalize translated text (fix diacritics, punctuation)."""
    normalizer = IndicNormalizer(lang_code)
    return normalizer.normalize(text)

def process_srt_file(input_file, output_file, target_lang="hi"):
    """Main function: Read SRT, translate, and save."""
    model, tokenizer = load_model_and_tokenizer()

    with open(input_file, "r", encoding="utf-8") as f:
        subtitles = list(srt.parse(f.read()))

    for sub in subtitles:
        translated_text = translate_text(model, tokenizer, sub.content, target_lang)
        sub.content = normalize_indic_text(translated_text, target_lang)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt.compose(subtitles))

if __name__ == "__main__":
    # Example usage
    input_srt = "sample.srt"    # Path to your English SRT file
    output_srt = "output.srt"  # Output file name
    target_language = "te"     # Language code (e.g., "hi" for Hindi, "ta" for Tamil)

    process_srt_file(input_srt, output_srt, target_language)
    print(f"Translation complete! Output saved to {output_srt}")

language_codes = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Odia": "or"
}