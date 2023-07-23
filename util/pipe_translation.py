from transformers import pipeline, Pipeline

translator: Pipeline = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-base-en-sh")
print(translator(">>srp_Cyrl<< You're about to make a very serious mistake."))

# expected output: Ti si o tome napraviti vrlo ozbiljnu pogrešku.

fp = open("opus-100/opus.en-sr-test.en", "r")
en_test_split = fp.read().splitlines()

# loading the model and translating test set again
padded_test_set = [">>srp_Latn<< " + sentence for sentence in en_test_split]
trans_sentences = translator(padded_test_set)
trans_file = open("raw_translation.txt", "w")
print("here")
for t in trans_sentences:
    print(t)
    trans_file.write(t["translation_text"]+"\n")
