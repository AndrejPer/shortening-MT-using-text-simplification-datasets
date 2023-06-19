from transformers import pipeline
pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-tc-base-en-sh")
print(pipe(">>cnr<< You're about to make a very serious mistake."))

# expected output: Ti si o tome napraviti vrlo ozbiljnu pogrešku.

fp = open("opus.en-sr-test.en")
en_test_split = fp.read().splitlines()

test_sentences = [sentence for sentence in en_test_split]
print("test set formed")

# loading the model and translating test set again
model_checkpoint = "./Helsinki-NLP/opus-mt-tc-base-en-sh"
print("loaded model")
padded_test_set = [">>>srp_Latn<<< " + sentence for sentence in test_sentences]
trans_file = open("raw_translation.txt", "w")
for t in padded_test_set:
    print(pipe(t), file=trans_file)
