from datasets import load_dataset
import argparse


dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "eng-srp_Cyrl")
print("here")



#print(len(dataset['test']['sourceString']))
sourceStrings = dataset['test']['sourceString'][:10]
print(sourceStrings)

parser = argparse.ArgumentParser()
parser.add_argument("--num_sentences", type = int, help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, help="Number of first X rules from PPDB instance to apply")
args = parser.parse_args()

print("Modifying", args.num_sentences, "sentences using", args.num_rules, "paraphrasing rules.")

for sentance in sourceStrings:
    words = sentance.split(" ")
    for word in words:
        print(word)
