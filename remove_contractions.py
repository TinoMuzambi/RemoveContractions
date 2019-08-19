# Tino Muzambi
# 2019/08/19 08:59
# Remove contractions from your essays


contractions = {"it's" : "it is", "i'll" : "i will", "won't" : "will not", "shan't" : "shall not"}
tall_contractions = {"It's" : "It is", "I'll" : "I will", "Won't" : "Will not", "Shan't" : "Shall not"}


def main():
    file_name = input("Enter the name of the file:\n")
    try:
        the_file = open(file_name, "r")
        words = the_file.read()
        words = words.split()
        print(words)
        for word in words:
            if word in contractions:
                print(contractions[word], end = " ")
            elif word in tall_contractions:
                print(tall_contractions[word], end = " ")
            elif "'s" in word:
                pre = word[0:word.find("'")]
                print(pre + " is", end = " ")
            else:
                print(word, end = " ")
    except FileNotFoundError:
        print("Where the file at tho?")


if __name__ == '__main__':
    main()
