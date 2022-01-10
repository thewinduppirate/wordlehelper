#! /usr/bin/python
# Shitty script to help solve Wordle puzzles

from PyDictionary import PyDictionary
import nltk
import re

# nltk.download('words')

from nltk.corpus import words

dictionary = PyDictionary()

# create set of words
setOfWords = set(words.words())

# create set of words 5 letters long
fiveLengthWords = [word for word in setOfWords if len(word) == 5]

# get list of known good letters from user
contains = input("What letters are known to be in the word?\n")

# simple sanity check for no more than 5 chars
if len(contains) > 5:
    print("You typed: "+contains)
    print("This is more than 5 characters, try again.")
    contains = input("What letters are known to be in the word?\n")

# tidy up input and convert to list
letters = list(contains.lower())

# candidates = [word for word in fiveLengthWords if letters in word]
candidates = []

for word in fiveLengthWords:
    if all([letter in word for letter in letters]):
        candidates.append(word)

# print("These are the current candidates:")
# print(candidates)
print("\n##############################\n")

raw_locations = input("What letter positions are known (green) using _ for\
                      unknowns?\n")

if len(raw_locations) > 5:
    print("You typed: "+raw_locations)
    print("This is more than 5 characters, try again.")
    raw_locations = input("What letters positions are known in the word using\
                           _ for unknowns?\n")

print("\n##############################\n")

locations = raw_locations.lower().replace("_", ".")

word_regex = locations

results = []

for word in candidates:
    bingo = re.search(word_regex, word)
    if hasattr(bingo, "group"):
        results.append(bingo.group())

print("Here are the final candidates:")
for word in results:
    try:
        defin = str(dictionary.meaning(word))
    except:
        defin = "Couldn't find a definition"

    print(word+": "+defin+"\n")
