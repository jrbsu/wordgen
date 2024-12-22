import sys, string
from modules import utils

def remove_punctuation(word):
    translation_table = str.maketrans('', '', string.punctuation)
    return word.translate(translation_table)

words = sys.argv
words.pop(0)
result = []
for word in words:
    word = remove_punctuation(word)
    result += "".join(utils.ipa_gen(utils.stress(word, True), is_syllables=True)).lower()
    result += " "

print("".join(result))