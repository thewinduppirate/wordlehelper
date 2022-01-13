#! /usr/bin/python
# Shitty script to help solve Wordle puzzles
from flask import Flask, request, render_template

from PyDictionary import PyDictionary
import nltk
import re
# from nltk.corpus import words

# init dictionary
dictionary = PyDictionary()

# create set of words
nltk.download('words')
words = nltk.corpus.words
all_words_set = set(words.words())

# create list of words 5 letters long
five_len_words = [word for word in all_words_set if len(word) == 5]


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def main_page():
        return render_template("input-form.html")

    @app.route("/", methods=["POST"])
    def main_page_post():
        warning = ""

        # get input from form
        raw_letters = request.form["letters"].lower()
        raw_positions = request.form.get("positions").lower()
        raw_exclude = request.form.get("exclude").lower()
        result_format = request.form.get("result_format")

        # Simple sanity check that we have some letters to work with
        if len(raw_letters) == 0:
            warning = "We need at least one letter to begin helping."
            return render_template('results.html',
                                   results=[],
                                   warning=warning)

        # checks position data
        if len(raw_positions) == 0:
            # assume no input means no knowns
            raw_positions = "_____"
        elif len(raw_positions) != 5:
            # render a warning if wrong number of positions
            warning = "Check your character positions"
            return render_template('results.html',
                                   results=[],
                                   warning=warning)

        # convert letters to list
        letters = list(raw_letters)
        exclude = list(raw_exclude)

        # start by creating empty list for words with 0 excluded letters
        not_excluded = []
        for word in five_len_words:
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
        results_list = []

        # cheat and change result format depending on number of results
        if len(results) > 5:
            warning = "Skipping definitions as there are a more than 5 potentials."
            warning += " ("+str(len(results))+")"
            result_format = "Words"

        if result_format == "Words":
            for word in results:
                results_list.append(word)

        elif result_format == "Definitions":
            count = 1
            for word in results:
                try:
                    defin = str(dictionary.meaning(word))
                except:
                    defin = "{Couldn't find a definition.}"

                if defin == "None":
                    defin = "{Couldn't find a definition.}"

                results_list.append("#"+str(count)+": "+defin)
                count += 1

        else:
            for word in results:
                try:
                    defin = str(dictionary.meaning(word))
                except:
                    defin = "{Couldn't find a definition.}"

                if defin == "None":
                    defin = "{Couldn't find a definition.}"

                results_list.append(word+": "+defin)

        return render_template('results.html',
                               results=results_list,
                               warning=warning)

    return app
