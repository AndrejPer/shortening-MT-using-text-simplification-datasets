from datasets import load_dataset, DatasetDict, Dataset

a_file = open("opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
test_sentences = [sentence for sentence in en_test_split]
test = Dataset.from_dict(test)

from transformers import pipeline

model_checkpoint = "Helsinki-NLP/opus-mt-tc-base-en-sh"
translator = pipeline("translation", model=model_checkpoint)
print(translator("Default to expanded threads"))
print(translator("Unable to import %1 using the OFX importer plugin. This file is not the correct format."))

# checking output of translation of test set before training and storing it in a file
test_translation = translator(test_sentences)
trans_file = open("raw_translation.txt", "w")
for sentence in test_translation:
    print(sentence)
    trans_file.write(sentence + "\n")
