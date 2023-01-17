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
