"""A small, privacy-friendly contraction expander."""

import re

from flask import Flask, jsonify, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

MAX_TEXT_LENGTH = 50_000

# Explicit phrases keep possessives such as "Tino's laptop" untouched. Ambiguous
# forms ending in 'd are expanded to "would", the most useful reading for prose.
CONTRACTIONS = {
    "ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "here's": "here is",
    "how'd": "how did",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "I would",
    "i'll": "I will",
    "i'm": "I am",
    "i've": "I have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "let's": "let us",
    "might've": "might have",
    "mightn't": "might not",
    "must've": "must have",
    "mustn't": "must not",
    "shan't": "shall not",
    "she'd": "she would",
    "she'll": "she will",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "somebody's": "somebody is",
    "someone's": "someone is",
    "something's": "something is",
    "that'd": "that would",
    "that'll": "that will",
    "that's": "that is",
    "there'd": "there would",
    "there'll": "there will",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'd": "what did",
    "what'll": "what will",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "where'd": "where did",
    "where's": "where is",
    "who'd": "who would",
    "who'll": "who will",
    "who's": "who is",
    "who've": "who have",
    "why'd": "why did",
    "why's": "why is",
    "won't": "will not",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have",
    "'tis": "it is",
    "'twas": "it was",
}

CONTRACTION_PATTERN = re.compile(
    r"(?<![\w'])((?:"
    + "|".join(re.escape(item) for item in sorted(CONTRACTIONS, key=len, reverse=True))
    + r"))(?![\w'])",
    re.IGNORECASE,
)


class InputForm(Form):
    uncontracted = TextAreaField(
        "Text",
        validators=[
            validators.InputRequired(message="Enter some text to expand."),
            validators.Length(
                max=MAX_TEXT_LENGTH,
                message=f"Keep the text under {MAX_TEXT_LENGTH:,} characters.",
            ),
        ],
    )


def _match_case(source: str, replacement: str) -> str:
    if source.isupper():
        return replacement.upper()
    if source[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def expand_contractions(text: str) -> tuple[str, int]:
    """Expand known English contractions without changing surrounding whitespace."""
    normalized = text.replace("’", "'")

    def replace(match: re.Match[str]) -> str:
        source = match.group(0)
        return _match_case(source, CONTRACTIONS[source.lower()])

    return CONTRACTION_PATTERN.subn(replace, normalized)

@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; style-src 'self'; "
        "font-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/", methods=["GET", "POST"])
def upload_files():
    form = InputForm(request.form)
    result = None
    replacement_count = 0
    if request.method == "POST" and form.validate():
        result, replacement_count = expand_contractions(form.uncontracted.data)
    return render_template(
        "index.html",
        form=form,
        result=result,
        replacement_count=replacement_count,
        max_text_length=MAX_TEXT_LENGTH,
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run()
