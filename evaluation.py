from transformers import MarianMTModel, MarianTokenizer
from datasets import DatasetDict, Dataset
from evaluate import evaluator
import evaluate

a_file = open("opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
test_sentences = [sentence for sentence in en_test_split]
test = Dataset.from_dict(test)

model_checkpoint = "./Helsinki-NLP/serbian-opus-mt-tc-base-en-sh"
model = MarianMTModel.from_pretrained(model_checkpoint)
metric = evaluate.load("sacrebleu")

task_evaluator = evaluator("translation")
results = task_evaluator.compute(model_or_pipeline=model, data=test, metric=metric,)

print(f"evaluation of sacrebleu of the model {model_checkpoint}:")
print(results)
