# Tino Muzambi
# 2019/08/19 08:59
# Remove contractions from your essays
import re

from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

contractions = {"won't": "will not", "shan't": "shall not", "isn't": "is not", "aren't": "are not",
                "wasn't": "was not", "weren't": "were not", "haven't": "have not", "hasn't": "has not",
                "hadn't": "had not", "wouldn't": "would not", "don't": "do not", "doesn't": "does not",
                "didn't": "did not", "can't": "cannot", "shouldn't": "should not", "mightn't": "might not",
                "mustn't": "must not", "couldn't": "could not", "'tis": "it is", "'twas": "it was",
                "ain't": "are not"}
tall_contractions = {"Won't": "Will not", "Shan't": "Shall not", "Isn't": "Is not", "Aren't": "Are not",
                     "Wasn't": "Was not", "Weren't": "Were not", "Haven't": "Have not", "Hasn't": "Has not",
                     "Hadn't": "Had not", "Wouldn't": "Would not", "Don't": "Do not", "Doesn't": "Does not",
                     "Didn't": "Did not", "Can't": "Cannot", "Shouldn't": "Should not", "Mightn't": "Might not",
                     "Mustn't": "Must not", "Couldn't": "Could not", "'Tis": "It is", "'Twas": "It was",
                     "Ain't": "Are not"}


class InputForm(Form):
    uncontracted = TextAreaField('Text', render_kw={"rows": 15, "cols": 100},
                                 validators=[validators.InputRequired()])


def process_file(words):
    result_file = ""
    count = 0
    words = words.replace("’", "'")  # Replace weird apostrophe with utf-8 version.
    delims = " ", "\r"
    pattern = "|".join(map(re.escape, delims))  # Join multiple different delimeters.
    words = re.split(pattern, words)
    for word in words:
        if word == "":                                          # Special cases for replacing contractions.
            result_file += "\n\n"
        elif "let's" in word:
            result_file += "let us" + " "
            count += 1
        elif "'s" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'s") + 2:]
            result_file += pre + " is" + post + " "
            count += 1
        elif "'ll" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'ll") + 3:]
            if pre == "i":
                pre = "I"
            result_file += pre + " will" + post + " "
            count += 1
        elif "'d" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'d") + 2:]
            if pre == "i":
                pre = "I"
            result_file += pre + " would" + post + " "
            count += 1
        elif "'ve" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'ve") + 3:]
            if pre == "i":
                pre = "I"
            result_file += pre + " have" + post + " "
            count += 1
        elif "'re" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'re") + 3:]
            result_file += pre + " are" + post + " "
            count += 1
        elif "'m" in word:
            pre = word[0:word.find("'")]
            post = word[word.find("'m") + 2:]
            if pre == "i":
                pre = "I"
            result_file += pre + " am" + post + " "
            count += 1
        elif word in contractions:                                        # Standard contraction replacement with dict.
            result_file += contractions[word] + " "
            count += 1
        elif word in tall_contractions:                   # Standard contraction replacement for uppercase with dict.
            result_file += tall_contractions[word] + " "
            count += 1
        else:
            result_file += word + " "                   # Else word isn't a contraction and it passes through.

    result_file += "\n\n" + str(count) + " replacements made."
    return result_file

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        result = process_file(form.uncontracted.data)
    else:
        result = None
    return render_template('index.html', form=form, result=result)


if __name__ == '__main__':
    app.run(debug=True)
