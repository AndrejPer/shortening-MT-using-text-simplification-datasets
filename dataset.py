from datasets import load_dataset
import argparse
import re
import pandas as pd

#PARSING
parser = argparse.ArgumentParser()
# Set the parameters
parser.add_argument("--num_sentences", type = int, default=1000000, help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, default=7007, help="Number of first X rules from PPDB instance to apply")
args = parser.parse_args()
print(f"Modifying {args.num_sentences} sentences using {args.num_rules} paraphrasing rules.")


#GETTING SOURCE SENTENCES
with open("opus-100/opus.en-sr-train.en") as f:
    lines = f.readlines()
    fields = [line.strip().split('\n') for line in lines]
    source_sentences = pd.DataFrame(fields)
print(source_sentences[0][10])


#APPLYING RULES
rules = pd.read_csv("sorted_ppdb_small.csv", delimiter='\|', engine='python')

# Counter for the number of changes made
counter = 0

for i, sentence in enumerate(source_sentences.to_numpy()):
    #print(f"doing sentence {i}")
    #print(sentence[0])
    for index in range(args.num_rules):
        # Making the pattern with whitespace, so it doesn't change 'Facebook' to 'Facebookay'
        pattern = re.compile(re.escape(" " + rules["Shorter"][index].strip() + " "))

        changes = len(re.findall(pattern, sentence[0]))
        if changes != 0:
            #print(changes)
            counter = counter + changes
            #print(f"Before: {sentence[0]}")
            sentence[0] = re.sub(pattern, " " + rules["Longer"][index].strip() + " ", sentence[0])
            #print(f"After: {sentence[0]}")

source_sentences.to_csv(f"opus_{args.num_rules}_{args.num_sentences}.en-sr-train.en", sep="\n")
print(counter)