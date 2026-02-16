import string


def process_line(line):
    # Remove punctuation signs
    line = line.translate(str.maketrans('', '', string.punctuation))

    # Split the line into words and remove whitespace
    words = [word.strip() for word in line.split()]

    return words


def lists_have_same_elements(list1, list2):
    return set(list1) == set(list2)


def count_total_words(words_list):
    return len(words_list)


def main(file_path1, file_path2):
    try:
        total_words_file1 = 0
        total_words_file2 = 0

        with open(file_path1, 'r') as file1, open(file_path2, 'r') as file2:
            for line1, line2 in zip(file1, file2):
                words1 = process_line(line1)
                words2 = process_line(line2)
                total_words_file1 += count_total_words(words1)
                total_words_file2 += count_total_words(words2)

                if not lists_have_same_elements(words1, words2):
                    print("File 1:", words1)
                    print("File 2:", words2)

        print("Total words in File 1:", total_words_file1)
        print("Total words in File 2:", total_words_file2)

    except FileNotFoundError:
        print("Error: One or both files were not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path1 = "../translations/old/short_XXL_translation.txt"  # Replace this with the path to the shortening text file
    file_path2 = "../translations/normal_translation.txt"  # Replace this with the path to the normal text file
    main(file_path1, file_path2)
