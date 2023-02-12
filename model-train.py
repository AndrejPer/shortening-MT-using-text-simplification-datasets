from datasets import load_dataset, DatasetDict, Dataset
import pandas as pd

a_file = open("opus_7007_1000000.en-sr-train.en")
file_contents = a_file.read()
en_train_split = file_contents.splitlines()
a_file = open("opus.en-sr-train.sr")
file_contents = a_file.read()
sr_train_split = file_contents.splitlines()

train = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_train_split, sr_train_split)]}
print(train['translation'][:10])


a_file = open("opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
print(test['translation'][:10])


a_file = open("opus.en-sr-dev.sr")
file_contents = a_file.read()
sr_dev_split = file_contents.splitlines()
a_file = open("opus.en-sr-dev.en")
file_contents = a_file.read()
en_dev_split = file_contents.splitlines()

dev = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_dev_split, sr_dev_split)]}
print(dev['translation'][:10])

dataset = dict({'train': train, 'test': test, 'dev': dev})
dataset = Dataset.from_dict(dataset)

from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
translator = pipeline("translation", model=model_checkpoint)
translator("Default to expanded threads")


translator(
    "Unable to import %1 using the OFX importer plugin. This file is not the correct format."
)

from transformers import AutoTokenizer

model_checkpoint = "Helsinki-NLP/opus-mt-en-fr"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, return_tensors="pt")

en_sentence = dataset["train"][1]["translation"]["en"]
sr_sentence = dataset["train"][1]["translation"]["sr"]

inputs = tokenizer(en_sentence, text_target=sr_sentence)
print(inputs)


max_length = 128


def preprocess_function(examples):
    inputs = [ex["en"] for ex in examples["translation"]]
    targets = [ex["fr"] for ex in examples["translation"]]
    model_inputs = tokenizer(
        inputs, text_target=targets, max_length=max_length, truncation=True
    )
    return model_inputs

tokenized_datasets = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset["train"].column_names,
)

from transformers import TFAutoModelForSeq2SeqLM
model = TFAutoModelForSeq2SeqLM.from_pretrained(model_checkpoint, from_pt=True)

from transformers import DataCollatorForSeq2Seq
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, return_tensors="tf")

batch = data_collator([tokenized_datasets["train"][i] for i in range(4, 6)])
print(batch.keys())

for i in range(4, 6):
    print(tokenized_datasets["train"][i]["labels"])

tf_train_dataset = model.prepare_tf_dataset(
    tokenized_datasets["train"],
    collate_fn=data_collator,
    shuffle=True,
    batch_size=32,
)
tf_eval_dataset = model.prepare_tf_dataset(
    tokenized_datasets["validation"],
    collate_fn=data_collator,
    shuffle=False,
    batch_size=16,
)

import evaluate

metric = evaluate.load("sacrebleu")

import numpy as np
import tensorflow as tf
from tqdm import tqdm

generation_data_collator = DataCollatorForSeq2Seq(
    tokenizer, model=model, return_tensors="tf", pad_to_multiple_of=128
)

tf_generate_dataset = model.prepare_tf_dataset(
    tokenized_datasets["validation"],
    collate_fn=generation_data_collator,
    shuffle=False,
    batch_size=8,
)


@tf.function(jit_compile=True)
def generate_with_xla(batch):
    return model.generate(
        input_ids=batch["input_ids"],
        attention_mask=batch["attention_mask"],
        max_new_tokens=128,
    )


def compute_metrics():
    all_preds = []
    all_labels = []

    for batch, labels in tqdm(tf_generate_dataset):
     predictions = generate_with_xla(batch)
     decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
     labels = labels.numpy()
     labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
     decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
     decoded_preds = [pred.strip() for pred in decoded_preds]
     decoded_labels = [[label.strip()] for label in decoded_labels]
     all_preds.extend(decoded_preds)
     all_labels.extend(decoded_labels)

     result = metric.compute(predictions=all_preds, references=all_labels)
     return {"bleu": result["score"]}

from transformers import create_optimizer
from transformers.keras_callbacks import PushToHubCallback
import tensorflow as tf

# The number of training steps is the number of samples in the dataset, divided by the batch size then multiplied
# by the total number of epochs. Note that the tf_train_dataset here is a batched tf.data.Dataset,
# not the original Hugging Face Dataset, so its len() is already num_samples // batch_size.
num_epochs = 3
num_train_steps = len(tf_train_dataset) * num_epochs

optimizer, schedule = create_optimizer(
    init_lr=5e-5,
    num_warmup_steps=0,
    num_train_steps=num_train_steps,
    weight_decay_rate=0.01,
)
model.compile(optimizer=optimizer)

# Train in mixed-precision float16
tf.keras.mixed_precision.set_global_policy("mixed_float16")


from transformers.keras_callbacks import PushToHubCallback

callback = PushToHubCallback(
    output_dir="marian-finetuned-kde4-en-to-fr", tokenizer=tokenizer
)

model.fit(
    tf_train_dataset,
    validation_data=tf_eval_dataset,
    callbacks=[callback],
    epochs=num_epochs,
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

trainer.train()
trainer.save_model(".")