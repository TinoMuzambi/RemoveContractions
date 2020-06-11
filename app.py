# Tino Muzambi
# 2019/08/19 08:59
# Remove contractions from your essays
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os


UPLOAD_FOLDER = './files/'
ALLOWED_EXTENSIONS = {'txt'}
MAX_SIZE = 30000000


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = MAX_SIZE


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


@app.route('/upload')
def upload_file():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_file(file_name):
    # file_name = input("Enter the name of the file:\n")
    # out_file = file_name[0 : file_name.find(".txt")] + " edited" + file_name[file_name.find(".") :]
    # output = open(out_file, "w")
    result_file = ""
    count = 0
    try:
        the_file = open(file_name, encoding="utf-8")
        words = the_file.read()
        words = words.replace("’", "'")
        the_file.close()
        words = words.split()
        for word in words:
            if "'s" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'s") + 2 :]
                result_file += pre + " is " + post + " "
                # print(pre + " is" + post, end = " ", file = output)
                count += 1
            elif "'ll" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ll") + 3 :]
                if pre == "i":
                    pre = "I"
                result_file += pre + " will " + post + " "
                # print(pre + " will" + post, end = " ", file = output)
                count += 1
            elif "'d" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'d") + 2 :]
                if pre == "i":
                    pre = "I"
                result_file += pre + " would " + post + " "
                # print(pre + " would" + post, end = " ", file = output)
                count += 1
            elif "'ve" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'ve") + 3 :]
                if pre == "i":
                    pre = "I"
                result_file += pre + " have " + post + " "
                # print(pre + " have" + post, end = " ", file = output)
                count += 1
            elif "'re" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'re") + 3 :]
                result_file += pre + " are " + post + " "
                # print(pre + " are" + post, end = " ", file = output)
                count += 1
            elif "'m" in word:
                pre = word[0:word.find("'")]
                post = word[word.find("'m") + 2 :]
                if pre == "i":
                    pre = "I"
                result_file += pre + " am " + post + " "
                # print(pre + " am" + post, end = " ", file = output)
                count += 1
            elif word in contractions:
                result_file += contractions[word] + " "
                # print(contractions[word], end = " ", file = output)
                count += 1
            elif word in tall_contractions:
                result_file += tall_contractions[word] + " "
                # print(tall_contractions[word], end = " ", file = output)
                count += 1
            else:
                result_file += word + " "
                # print(word, end = " ", file = output)
    except FileNotFoundError:
        print("File not found. Ensure you've typed the file name (as well as the file extension) correctly.")
    # output.close()
    # print("Output file \"" + out_file + "\" written to successfully.")

    result_file += "\n\n" + str(count) + " replacements made."
    return result_file


@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = process_file("./files/" + filename)
            return render_template('index.html', result=result)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
