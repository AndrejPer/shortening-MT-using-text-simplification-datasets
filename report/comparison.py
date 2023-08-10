
raw = open("../opus-100/opus.en-sr-train.en", "r")
raw_lines = raw.readlines()
raw.close()
raw_trans = "".join(raw_lines)

fine = open("../sorted_ppdb", "r")
fine_lines = fine.readlines()
fine.close()
fine_trans = "".join(fine_lines)

raw_count = len(list(filter(str.isalnum, raw_trans)))
fine_count = len(list(filter(str.isalnum, fine_trans)))

ratio = (raw_count - fine_count) / raw_count
print(ratio)
print(f"fine:{fine_count}\nraw:{raw_count}\ndiff:{raw_count - fine_count}")
