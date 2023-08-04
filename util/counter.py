def count_words(filename):
    word_counts_name1 = {'**': 0, '*': 0, '-': 0, 'missT': 0, 'missW': 0}
    word_counts_name2 = {'**': 0, '*': 0, '-': 0, 'missT': 0, 'missW': 0}
    with open(filename, 'r') as file:
        for line in file:
            #print(line)
            id_, name, words = line.strip().split('\t')
            print(f"{id_}, {name}, {words}")
            if name == 'normout.txt':
                for word in words.split():
                    print(f"{word} is one")
                    if word in word_counts_name1:
                        word_counts_name1[word] += 1
            elif name == 'shortout.txt':
                for word in words.split():
                    print(f"{word} is one")
                    if word in word_counts_name2:
                        word_counts_name2[word] += 1
    return word_counts_name1, word_counts_name2


# Provide the path to your input file
filename = '/Users/Andrej/Documents/Fac/MT/quickjudge/annot_res.txt'
word_counts_name1, word_counts_name2 = count_words(filename)

# Print the word counts for name1
print("Word counts for name1:")
for word, count in word_counts_name1.items():
    print(f'{word}: {count/55*100}')

print()  # Add a line break

# Print the word counts for name2
print("Word counts for name2:")
for word, count in word_counts_name2.items():
    print(f'{word}: {count/55*100}')
