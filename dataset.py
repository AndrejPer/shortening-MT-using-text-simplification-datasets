from datasets import load_dataset
import argparse
import re
import pandas as pd

# PARSING
parser = argparse.ArgumentParser()
# Set the parameters
parser.add_argument("--num_sentences", type=int, default=1000000,
                    help="Number of first Y source sentences to apply rules to")
parser.add_argument("--num_rules", type=int, default=1000, help="Number of first X rules from PPDB instance to apply")

parser.add_argument("--input_file", type=str, default="opus-100/opus.en-sr-train.en", help="Training set for Eng->Sr")
parser.add_argument("--output_path", type=str, default="./", help="")
parser.add_argument("--csv_file", type=str, default="sorted_ppdb_small.csv", help="CSV file with the rules")
args = parser.parse_args()

print(f"Modifying {args.num_sentences} sentences using {args.num_rules} paraphrasing rules.")

input_file = open(args.input_file)
lines = input_file.readlines()[:args.num_sentences]
input_file.close()

text = "".join(lines)

rules = pd.read_csv(args.csv_file, delimiter="\|", nrows=args.num_rules, engine="python")

counter = 0
for i, rule in rules.iterrows():
    # Ignoring numbers because they appear in contexts of dates, orders, within other numbers...
    # - it does not much sense to replace them
    if rule["Shorter"].strip().isnumeric():
        continue

    # Using `\b` for detecting word boundaries
    text, n = re.subn("\\b" + rule["Shorter"].strip() + "\\b", rule["Longer"].strip(), text)

    # Info logging, so we see the state of our computation
    if n != 0:
        print(f"Applying {i}. rule: ({rule.Shorter.strip()} -> {rule.Longer.strip()}) with {n} replacements")

    counter += n

print(f"Number of replacements: {counter}")

output_file = open(f"{args.output_path}/opus_{args.num_rules}_{args.num_sentences}.en-sr-train.en", "w")
output_file.write(text)
output_file.close()