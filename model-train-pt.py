from datasets import load_dataset, DatasetDict, Dataset
import pandas as pd


a_file = open("opus_7007_1000000.en-sr-train.en")
file_contents = a_file.read()
en_train_split = file_contents.splitlines()
a_file = open("opus.en-sr-train.sr")
file_contents = a_file.read()
sr_train_split = file_contents.splitlines()

train = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_train_split, sr_train_split)]}
train = Dataset.from_dict(train)


a_file = open("opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
test = Dataset.from_dict(test)


a_file = open("opus.en-sr-dev.sr")
file_contents = a_file.read()
sr_dev_split = file_contents.splitlines()
a_file = open("opus.en-sr-dev.en")
file_contents = a_file.read()
en_dev_split = file_contents.splitlines()

dev = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_dev_split, sr_dev_split)]}
dev = Dataset.from_dict(dev)

dataset = DatasetDict({'train': train, 'test': test, 'validation': dev})

from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-tc-base-en-sh"
translator = pipeline("translation", model=model_checkpoint)
translator("Default to expanded threads")


translator(
    "Unable to import %1 using the OFX importer plugin. This file is not the correct format."
)

from transformers import AutoTokenizer

model_checkpoint = "Helsinki-NLP/opus-mt-tc-base-en-sh"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, return_tensors="pt")

en_sentence = dataset["train"][1]["translation"]["en"]
sr_sentence = dataset["train"][1]["translation"]["sr"]

inputs = tokenizer(en_sentence, text_target=sr_sentence)
print(inputs)


max_length = 128


def preprocess_function(examples):
    inputs = [ex["en"] for ex in examples["translation"]]
    targets = [ex["sr"] for ex in examples["translation"]]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs

tokenized_datasets = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)

from transformers import AutoModelForSeq2SeqLM
model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)

from transformers import DataCollatorForSeq2Seq
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

batch = data_collator([tokenized_datasets["train"][i] for i in range(4, 6)])
print(batch.keys())

for i in range(4, 6):
    print(tokenized_datasets["train"][i]["labels"])



import evaluate
metric = evaluate.load("sacrebleu")

import numpy as np

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    # In case the model returns more than the prediction logits
    if isinstance(preds, tuple):
        preds = preds[0]

    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100s in the labels as we can't decode them
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [[label.strip()] for label in decoded_labels]

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    return {"bleu": result["score"]}

from transformers import Seq2SeqTrainingArguments

args = Seq2SeqTrainingArguments(
    f"Helsinki-NLP/finetuned-opus-mt-tc-base-en-sh",
    evaluation_strategy="no",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=3,
    predict_with_generate=True,
    fp16=True,
)

from transformers import Seq2SeqTrainer

trainer = Seq2SeqTrainer(
    model,
    args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

print(trainer.evaluate(max_length=max_length))

trainer.train()
trainer.save_model(".")
