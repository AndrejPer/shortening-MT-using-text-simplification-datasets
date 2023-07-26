from transformers import MarianMTModel, MarianTokenizer

fp = open("opus.en-sr-test.en")
en_test_split = fp.read().splitlines()

test_sentences = [sentence for sentence in en_test_split]

# loading the model and translating test set again
model_checkpoint = "./Helsinki-NLP/shortL-opus-mt-tc-base-en-sh"
print("model named")
tokenizer = MarianTokenizer.from_pretrained(model_checkpoint)
print("tokenizer done")
model = MarianMTModel.from_pretrained(model_checkpoint)
print("model loaded")
padded_test_set = [">>srp_Latn<< " + sentence for sentence in test_sentences]
translated = model.generate(**tokenizer(test_sentences,
                                        return_tensors="pt", padding=True), max_length=256)
trans_file = open("short_L_translation.txt", "w")
for t in translated:
    trans_file.write(tokenizer.decode(t, skip_special_tokens=True) + "\n")

trans_file.close()