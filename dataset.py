from datasets import load_dataset


dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "eng-srp_Cyrl")
print("here")

first10 = dataset['test'][slice(10, None, None)]
print(first10)
