from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-tc-base-en-sh")

model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-tc-base-en-sh")