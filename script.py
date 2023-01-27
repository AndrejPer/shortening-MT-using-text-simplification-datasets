print("start")
fp = open("mock", "r")
fnew = open("relabeled_ppdb_small.csv", "w")
while True:
    line = fp.readline()
    if not line:
        break
    pars_line = line.split(" ||| ")
    if(len(pars_line) < 6):
        print(pars_line)
        break
    shorter = ""
    longer = ""

    if len(pars_line[1]) > len(pars_line[2]):
        shorter = pars_line[2]
        longer = pars_line[1]
    else:
        shorter = pars_line[1]
        longer = pars_line[2]

    print(len(pars_line))
    fnew.write(pars_line[0] + " ||| " + longer + " ||| " + shorter + " ||| " + pars_line[4] + " ||| " + str(len(shorter) / len(longer)) + " ||| " + pars_line[5])

#print(ratios)
print("end")
fp.close()
fnew.close()



##################################
import pandas as pd

df = pd.read_csv("relabeled_ppdb_small.csv", delimiter='\|\|\|', engine='python')
df = df.drop_duplicates()

# Sort the dataframe by the value of the fifth field in ascending order
df = df.sort_values(by=df.columns[4])

df.to_csv("sorted_ppdb_small.csv", sep='|', index=False)

######################################
from datasets import load_dataset
import argparse
import re

#PARSING
parser = argparse.ArgumentParser()
parser.add_argument("--num_sentences", type = int, help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, help="Number of first X rules from PPDB instance to apply")
args = parser.parse_args()

print("Modifying", args.num_sentences, "sentences using", args.num_rules, "paraphrasing rules.")


#GETTING SOURCE SENTENCES
#dataset = load_dataset("Helsinki-NLP/tatoeba_mt", "eng-srp_Cyrl")
#sourceStrings = dataset['test']['sourceString'][:args.num_sentences]
sourceStrings = ['A cat is not a person!', 'Actions speak louder than words.', 'Add more water to it.', "A dream... I was trying to explain to St. Peter, and was doing it in the German tongue, because I didn't want to be too explicit.", 'After long reflection, I decided to take things as they come.', 'After silence, that which comes nearest to expressing the inexpressible is music.', 'After three years of work by volunteers, the system has been fully repaired.', 'After you.', 'A gluten-free diet is the most effective treatment for coeliac disease.', 'A golden key opens all doors.']
print(sourceStrings)

#LOADING RULES
frules = open("sorted_ppdb_small.csv", "r")
rules = []
for i in range(args.num_rules):
    line = frules.readline()
    #in case of illegal argument
    if not line:
        break
    pars_line = line.split("|")
    rules.append({"tag": pars_line[0], "longer": pars_line[1], "shorter": pars_line[2], "score": float(pars_line[3]), "ratio": pars_line[4], "equivalence": pars_line[5]}) #dictionary of rules!
print(rules)


#APPLYING RULES
for sentence in sourceStrings:
    for rule in rules:
        if rule["shorter"] == "$":
            pattern = re.compile(r"\$")
        else:
            pattern = re.compile(rule["shorter"])
        print(re.findall(pattern, sentence))
        sentence = re.sub(pattern, rule["longer"], sentence)
        print(sentence)
