from datasets import load_dataset
import argparse
import re
import pandas as pd

#PARSING
parser = argparse.ArgumentParser()
parser.add_argument("--num_sentences", type = int, help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, help="Number of first X rules from PPDB instance to apply")
args = parser.parse_args()

print("Modifying", args.num_sentences, "sentences using", args.num_rules, "paraphrasing rules.")


#GETTING SOURCE SENTENCES
dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "eng-srp_Cyrl")
sourceStrings = dataset['test']['sourceString'][:args.num_sentences]
sourceStrings = ['A cat is not a person!', 'Actions speak louder than words.', 'Add more water to it.', "A dream... I was trying to explain to St. Peter, and was doing it in the German tongue, because I didn't want to be too explicit.", 'After long reflection, I decided to take things as they come.', 'After silence, that which comes nearest to expressing the inexpressible is music.', 'After three years of work by volunteers, the system has been fully repaired.', 'After you.', 'A gluten-free diet is the most effective treatment for coeliac disease.', 'A golden key opens all doors.']
print(sourceStrings)


#APPLYING RULES
column_names = ['Tag', 'Longer', 'Shorter', 'Score', 'Ratio', 'Equivalence']
df = pd.read_csv("sorted_ppdb_small.csv", delimiter='\|', engine='python', names=column_names)

for sentence in sourceStrings:
    for index in range(args.num_rules):
        if df["Shorter"][index] == "$":
            pattern = re.compile(r"\$")
        else:
            pattern = re.compile(df["Shorter"][index])
        print(re.findall(pattern, sentence))
        sentence = re.sub(pattern, df["Longer"][index], sentence)
        print(sentence)
