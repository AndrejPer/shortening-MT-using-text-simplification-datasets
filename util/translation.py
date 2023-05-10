from transformers import MarianMTModel, MarianTokenizer

a_file = open("opus.en-sr-test.en")
file_contents = a_file.read()
en_test_split = file_contents.splitlines()

test_sentences = [sentence for sentence in en_test_split]
print("test set formed")

# loading the model and translating test set again
model_checkpoint = "./Helsinki-NLP/shortS-opus-mt-tc-base-en-sh"
tokenizer = MarianTokenizer.from_pretrained(model_checkpoint)
model = MarianMTModel.from_pretrained(model_checkpoint)
print("loaded model")
padded_test_set = [">>>srp_Latn<<< " + sentence for sentence in test_sentences]
translated = model.generate(**tokenizer(test_sentences, return_tensors="pt", padding=True))
trans_file = open("corrected_short_translation.txt", "w")
for t in translated:
    print(tokenizer.decode(t, skip_special_tokens=True) + "\n")
    trans_file.write(tokenizer.decode(t, skip_special_tokens=True) + "\n")
