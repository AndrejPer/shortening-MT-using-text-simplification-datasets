import argparse
import re
import pandas as pd

# PARSING
parser = argparse.ArgumentParser()
# Set the parameters
parser.add_argument("--num_sentences", type=int, default=1000000,
                    help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, default=1000, help="Number of first X rules from PPDB instance to apply")

parser.add_argument("--input_file", type=str, default="../opus-100/opus.en-sr-train.en", help="Training set for Eng->Sr")
parser.add_argument("--output_path", type=str, default="./", help="")
parser.add_argument("--csv_file", type=str, default="../sorted_ppdb/sorted_ppdb_s_lexical.csv", help="CSV file with the rules")
args = parser.parse_args()

report_file = open("report_small_lexical_app.txt", "w")
print(f"Modifying {args.num_sentences} sentences using {args.num_rules} paraphrasing rules.")
print(f"Modifying {args.num_sentences} sentences using {args.num_rules} paraphrasing rules.", file=report_file)

input_file = open(args.input_file)

lines = input_file.readlines()[:args.num_sentences]
input_file.close()

text = "".join(lines)

rules = pd.read_csv(args.csv_file, delimiter="\|", nrows=args.num_rules, engine="python")

counter = 0
for i, rule in rules.iterrows():
    # Ignoring numbers because they appear in contexts of dates, orders, within other numbers...
    # - it does not much sense to replace them
    if rule["Shorter"].strip().isnumeric() \
            or rule["Ratio"] == "1.0" \
            or rule["Shorter"].strip() + "ing" == rule["Longer"].strip():
            # or rule["Tag"]=="NNS" and (rule["Shorter"].strip()[:-1] != 's' and rule["Longer"].strip() != 's'):
        continue

    # Using `\b` for detecting word boundaries
    text, n = re.subn("\\b" + rule["Shorter"].strip() + "\\b", rule["Longer"].strip(), text)

    # Info logging, so we see the state of our computation
    if n != 0:
        print(f"Applying {i}. rule: ({rule.Shorter.strip()} -> {rule.Longer.strip()}) with {n} replacements")
        print(f"Applying {i}. rule: ({rule.Shorter.strip()} -> {rule.Longer.strip()}) with {n} replacements", file=report_file)

    counter += n

print(f"Number of replacements: {counter}")

#output_file = open(f"{args.output_path}/opus_{args.num_rules}_{args.num_sentences}.en-sr-train.en", "w")
output_file = open(f"opus_{args.num_rules}_{args.num_sentences}.en-sr-train.en", "w")
output_file.write(text)
output_file.close()
report_file.close()