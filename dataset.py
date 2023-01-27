from datasets import load_dataset
import argparse
import re
import pandas as pd

#PARSING
parser = argparse.ArgumentParser()
parser.add_argument("--num_sentences", type = int, default=50, help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, default=100, help="Number of first X rules from PPDB instance to apply")
args = parser.parse_args()

print(f"Modifying {args.num_sentences} sentences using {args.num_rules}, paraphrasing rules.")


#GETTING SOURCE SENTENCES
dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "eng-srp_Cyrl")
source_sentences = dataset['validation']['sourceString'][:args.num_sentences]
#source_strings = ['A cat is not a person!', 'Actions speak louder than words.', 'Add more water to it.', "A dream... I was trying to explain to St. Peter, and was doing it in the German tongue, because I didn't want to be too explicit.", 'After long reflection, I decided to take things as they come.', 'After silence, that which comes nearest to expressing the inexpressible is music.', 'After three years of work by volunteers, the system has been fully repaired.', 'After you.', 'A gluten-free diet is the most effective treatment for coeliac disease.', 'A golden key opens all doors.']



#APPLYING RULES
df = pd.read_csv("sorted_ppdb_small.csv", delimiter='\|', engine='python')

# Counter for the number of changes made
counter = 0

for sentence in source_sentences:
    for index in range(args.num_rules):
        pattern = re.compile(re.escape(df["Shorter"][index].strip()))

        #print(len(re.findall(pattern, sentence)))
        counter = counter + len(re.findall(pattern, sentence))

        sentence = re.sub(pattern, df["Longer"][index], sentence)
        print(sentence)

print(counter)