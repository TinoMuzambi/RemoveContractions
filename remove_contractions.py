# Tino Muzambi
# 2019/08/19 08:59
# Remove contractions from your essays

import docx

contractions = {"won't" : "will not", "shan't" : "shall not", "isn't" : "is not", "aren't" : "are not",
                "wasn't" : "was not", "weren't" : "were not", "haven't" : "have not", "hasn't" : "has not",
                "hadn't" : "had not", "wouldn't" : "would not", "don't" : "do not", "doesn't" : "does not",
                "didn't" : "did not", "can't" : "cannot", "shouldn't" : "should not", "mightn't" : "might not",
                "mustn't" : "must not", "couldn't" : "could not", "'tis" : "it is", "'twas" : "it was",
                "ain't" : "are not"}
tall_contractions = {"Won't" : "Will not", "Shan't" : "Shall not", "Isn't" : "Is not", "Aren't" : "Are not",
                     "Wasn't" : "Was not", "Weren't" : "Were not", "Haven't" : "Have not", "Hasn't" : "Has not",
                     "Hadn't" : "Had not", "Wouldn't" : "Would not", "Don't" : "Do not", "Doesn't" : "Does not",
                     "Didn't" : "Did not", "Can't" : "Cannot", "Shouldn't" : "Should not", "Mightn't" : "Might not",
                     "Mustn't" : "Must not", "Couldn't" : "Could not", "'Tis" : "It is", "'Twas" : "It was",
                     "Ain't" : "Are not"}


def read_file(file_name):
    if file_name[file_name.find(".") :] == ".txt":
        the_file = open(file_name, "r")
        return the_file.read().split()
    elif file_name[file_name.find(".") :] == ".docx" or file_name[file_name.find(".") :] == ".doc":
        doc = docx.Document(file_name)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return '\n'.join(text).split()
    else:
        return []


def main():
    file_name = input("Enter the name of the file:\n")
    words = read_file(file_name)
    out_file = file_name[0 : file_name.find(".txt")] + " edited" + file_name[file_name.find(".") :]
    output = open(out_file, "w")
    count = 0
    try:
        the_file = open(file_name, "r")
        words = the_file.read()
        the_file.close()
        words = words.split()
        for word in words:
            if "'s" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'s") + 2 :]
                print(pre + " is" + post, end = " ", file = output)
                count += 1
            elif "'ll" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ll") + 3 :]
                if pre == "i":
                    pre = "I"
                print(pre + " will" + post, end = " ", file = output)
                count += 1
            elif "'d" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'d") + 2 :]
                if pre == "i":
                    pre = "I"
                print(pre + " would" + post, end = " ", file = output)
                count += 1
            elif "'ve" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ve") + 3 :]
                if pre == "i":
                    pre = "I"
                print(pre + " have" + post, end = " ", file = output)
                count += 1
            elif "'re" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'re") + 3 :]
                print(pre + " are" + post, end = " ", file = output)
                count += 1
            elif "'m" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'m") + 2 :]
                if pre == "i":
                    pre = "I"
                print(pre + " am" + post, end = " ", file = output)
                count += 1
            elif word in contractions:
                print(contractions[word], end = " ", file = output)
                count += 1
            elif word in tall_contractions:
                print(tall_contractions[word], end = " ", file = output)
                count += 1
            else:
                print(word, end = " ", file = output)
    except FileNotFoundError:
        print("File not found. Ensure you've typed the file name (as well as the file extension) correctly.")
    output.close()
    print("Output file \"" + out_file + "\" written to successfully.")
    print(str(count) + " replacements made.")


if __name__ == '__main__':
    main()
