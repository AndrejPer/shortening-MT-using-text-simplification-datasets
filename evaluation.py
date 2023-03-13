from transformers import MarianMTModel, MarianTokenizer
from datasets import DatasetDict, Dataset
from evaluate import evaluator
import evaluate

a_file = open("opus.en-sr-train.en")
file_contents = a_file.read()
en_train_split = file_contents.splitlines()
a_file = open("opus.en-sr-train.sr")
file_contents = a_file.read()
sr_train_split = file_contents.splitlines()

train = {
    'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_train_split, sr_train_split)]}
train = Dataset.from_dict(train)

a_file = open("opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
test_sentences = [sentence for sentence in en_test_split]
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

model_checkpoint = "./Helsinki-NLP/serbian-opus-mt-tc-base-en-sh"
model = MarianMTModel.from_pretrained(model_checkpoint)
metric = evaluate.load("sacrebleu")

task_evaluator = evaluator("translation")
results = task_evaluator.compute(model_or_pipeline=model, data=dataset, metric=metric,)

print(f"evaluation of sacrebleu of the model {model_checkpoint}:")
print(results)
