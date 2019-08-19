# Tino Muzambi
# 2019/08/19 08:59
# Remove contractions from your essays


contractions = {"won't" : "will not", "shan't" : "shall not", "isn't" : "is not", "aren't" : "are not",
                "wasn't" : "was not", "weren't" : "were not", "haven't" : "have not", "hasn't" : "has not",
                "hadn't" : "had not", "wouldn't" : "would not", "don't" : "do not", "doesn't" : "does not",
                "didn't" : "did not", "can't" : "cannot", "shouldn't" : "should not", "mightn't" : "might not",
                "mustn't" : "must not"}
tall_contractions = {"Won't" : "Will not", "Shan't" : "Shall not", "Isn't" : "Is not", "Aren't" : "Are not",
                     "Wasn't" : "Was not", "Weren't" : "Were not", "Haven't" : "Have not", "Hasn't" : "Has not",
                     "Hadn't" : "Had not", "Wouldn't" : "Would not", "Don't" : "Do not", "Doesn't" : "Does not",
                     "Didn't" : "Did not", "Can't" : "Cannot", "Shouldn't" : "Should not", "Mightn't" : "Might not",
                     "Mustn't" : "Must not"}


def main():
    file_name = input("Enter the name of the file:\n")
    out_file = file_name[0:file_name.find(".txt")] + "edited.txt"
    count = 0
    try:
        the_file = open(file_name, "r")
        words = the_file.read()
        print(words)
        words = words.split()
        for word in words:
            if "'s" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'s") + 2:]
                print(pre + " is" + post, end = " ")
                count += 1
            elif "'ll" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ll") + 3:]
                print(pre + " will" + post, end = " ")
                count += 1
            elif "'d" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'d") + 2:]
                print(pre + " would" + post, end = " ")
                count += 1
            elif "'ve" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ve") + 3:]
                print(pre + " have" + post, end = " ")
                count += 1
            elif "'re" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'re") + 3:]
                print(pre + " are" + post, end = " ")
                count += 1
            elif "'m" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'m") + 2:]
                print(pre + " am" + post, end = " ")
                count += 1
            elif word in contractions:
                print(contractions[word], end = " ")
                count += 1
            elif word in tall_contractions:
                print(tall_contractions[word], end = " ")
                count += 1
            else:
                print(word, end = " ")
    except FileNotFoundError:
        print("Where the file at tho?")
    print()
    print(str(count) + " replacements made.")


if __name__ == '__main__':
    main()
