from datasets import load_dataset, Dataset, DatasetDict
import pandas as pd

a_file = open("opus-100/opus_7007_1000000.en-sr-train.en")
file_contents = a_file.read()
en_train_split = file_contents.splitlines()
a_file = open("opus-100/opus.en-sr-train.sr")
file_contents = a_file.read()
sr_train_split = file_contents.splitlines()

train = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_train_split, sr_train_split)]}
# print(train['translation'][:10])


a_file = open("opus-100/opus.en-sr-test.sr")
file_contents = a_file.read()
sr_test_split = file_contents.splitlines()
a_file = open("opus-100/opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_test_split, sr_test_split)]}
# print(test['translation'][:10])


a_file = open("opus-100/opus.en-sr-dev.sr")
file_contents = a_file.read()
sr_dev_split = file_contents.splitlines()
a_file = open("opus-100/opus.en-sr-dev.en")
file_contents = a_file.read()
en_dev_split = file_contents.splitlines()

dev = {'translation': [{"en": eng_text, "sr": srb_text} for eng_text, srb_text in zip(en_dev_split, sr_dev_split)]}
# print(dev['translation'][:10])

dataset = DatasetDict({'train': train, 'test': test, 'dev': dev})
#dataset = Dataset.from_dict(dataset)


print(dataset)


