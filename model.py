from datasets import load_dataset
dataset = load_dataset("csv", data_files={"train": ["opus-100/opus.en-sr-train.en", "opus-100/opus.en-sr-train.sr"], "test": ["opus-100/opus.en-sr-test.en", "opus-100/opus.en-sr-test.sr"], "dev": ["opus-100/opus.en-sr-dev.en", "opus-100/opus.en-sr-dev.sr"]})

print(dataset)


