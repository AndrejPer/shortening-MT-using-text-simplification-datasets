s = "Nice. To. Meet. You."
print(len(list(filter(str.isalpha, s))))

raw = open("translations/raw_translation.txt", "r")
raw_lines = raw.readlines()
raw.close()
raw_trans = "".join(raw_lines)

fine = open("translations/fine-tuned_translation.txt", "r")
fine_lines = fine.readlines()
fine.close()
fine_trans = "".join(fine_lines)

raw_count = len(list(filter(str.isalpha, raw_trans)))
fine_count = len(list(filter(str.isalpha, fine_trans)))

ratio = (fine_count) / raw_count
print(ratio)
