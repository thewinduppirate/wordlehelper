#! /usr/bin/python
# Shitty script to help solve Wordle puzzles
from flask import Flask, request, render_template

from PyDictionary import PyDictionary
import nltk
import re
from nltk.corpus import words

# init dictionary
dictionary = PyDictionary()
# create set of words
setOfWords = set(words.words())
# create list of words 5 letters long
fiveLengthWords = [word for word in setOfWords if len(word) == 5]

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("input-form.html")


@app.route("/", methods=["POST"])
def main_page_post():
    raw_letters = request.form["letters"].lower()
    raw_positions = request.form.get("positions").lower()
    if len(raw_positions) == 0:
        raw_positions = "_____"
    elif len(raw_positions) != 5:
        return "Check your character positions"
    raw_exclude = request.form.get("exclude").lower()
    just_hints = request.form.get("just_hints")

    # convert letters to list
    letters = list(raw_letters)
    exclude = list(raw_exclude)

    not_excluded = []
    for word in fiveLengthWords:
        if not any([letter in word for letter in exclude]):
            not_excluded.append(word)

    # iterate through 5 letter words appending words that have all letters in
    # them
    candidates = []
    for word in not_excluded:
        if all([letter in word for letter in letters]):
            candidates.append(word)

    word_regex = raw_positions.replace("_", ".")

    # interate through candiate short list using regex find matches to
    # create final results from
    results = []
    for word in candidates:
        bingo = re.search(word_regex, word)
        if hasattr(bingo, "group"):
            results.append(bingo.group())

    # create final results list to return to user
    results_string = []
    warning = ""

    if just_hints:
        if len(results) > 10:
            warning = "Skipping definitions as there are a more than 10 potentials."
        else:
            count = 1
            for word in results:
                try:
                    defin = str(dictionary.meaning(word))
                except:
                    defin = "{Couldn't find a definition.}"

                if defin == "None":
                    defin = "{Couldn't find a definition.}"

                results_string.append("#"+str(count)+": "+defin)
                count += 1

    elif len(results) > 5:
        warning = "Skipping definitions as there are more than 5 potentials."
        for word in results:
            results_string.append(word)

    else:
        for word in results:
            try:
                defin = str(dictionary.meaning(word))
            except:
                defin = "{Couldn't find a definition.}"

            if defin == "None":
                defin = "{Couldn't find a definition.}"

            results_string.append(word+": "+defin)

    return render_template('results.html',
                           results=results_string,
                           warning=warning)
