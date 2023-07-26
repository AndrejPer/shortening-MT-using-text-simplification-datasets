import argparse
import re
import pandas as pd


def has_letter(input_string):
    return bool(re.search(r'[a-zA-Z]', input_string))


def has_punctuation(input_string):
    return bool(re.search(r'[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', input_string)) # all punctuation signs besides "-"


# PARSING
parser = argparse.ArgumentParser()
# Set the parameters
parser.add_argument("--num_sentences", type=int, default=1000000,
                    help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, default=1000, help="Number of first X rules from PPDB instance to apply")

parser.add_argument("--input_file", type=str, default="opus.en-sr-train.en", help="Training set for Eng->Sr")
parser.add_argument("--output_path", type=str, default="./", help="")
parser.add_argument("--csv_file", type=str, default="sorted_ppdb_xl_lexical.csv", help="CSV file with the rules")
args = parser.parse_args()

print(f"Modifying {args.num_sentences} sentences using {args.num_rules} paraphrasing rules.")

input_file = open(args.input_file)

lines = input_file.readlines()[:args.num_sentences]
input_file.close()

text = "".join(lines)

rules = pd.read_csv(args.csv_file, delimiter="\|", nrows=args.num_rules, engine="python")
print(f"Starting application of {len(rules)} rules")

counter = 0
for i, rule in rules.iterrows():
    # Ignoring numbers because they appear in contexts of dates, orders, within other numbers...
    # - any rule that does not have characters
    # - has any punct sign besides "-_
    # - they are the same length
    # - they are not a "turn -> turning" type og rule
    # - they wrongly paraphrase plurals
    if type(rule["Shorter"]) is not str \
            or not has_letter(rule["Shorter"].strip()) \
            or rule["Ratio"] == "1.0" \
            or rule["Shorter"].strip() + "ing" == rule["Longer"].strip() \
            or rule["Shorter"].strip() + rule["Shorter"].strip()[-1] + "ing" == rule["Longer"].strip() \
            or rule["Tag"] == "NNS" and (rule["Shorter"].strip()[-1] != 's' and rule["Longer"].strip()[-1] != 's'):
        # print(f"Continued for {i} ({rule['Shorter']} -> {rule['Longer']})")
        continue

    # Using `\b` for detecting word boundaries
    # Using replace(), so that a dot is not interpreted as wildcard
    text, n = re.subn("\\b" + rule["Shorter"].replace('.', '\.').strip() + "\\b", rule["Longer"].strip(), text)

    # Info logging, so we see the state of our computation
    if n != 0:
        print(f"Applying {i}. rule: ({rule.Shorter.strip()} -> {rule.Longer.strip()}) with {n} replacements")

    counter += n

print(f"Number of replacements: {counter}")

# output_file = open(f"{args.output_path}/opus_{args.num_rules}_{args.num_sentences}.en-sr-train.en", "w")
output_file = open(f"opus_{args.num_rules}_{args.num_sentences}_xl.en-sr-train.en", "w")
output_file.write(text)
output_file.close()
