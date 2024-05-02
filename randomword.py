import random, sys, re
from modules import data_retrieval

dict_words = []
onsets = ["tt","c","d","g","j","k","l","m","n","kk","r","s","t","v","f","x","z"]
vowels = ["a","e","i","o"]
codas = ["c","d","g","k","l","n","r","s","t","x","z"]
fricatives = ["c","j","l","r","s","v","w","x","z"]
ejectives = ["kk", "tt"]
gen_words = {
    2: [],
    3: [],
    4: [],
    5: []
}
gw_len = 0

arguments = sys.argv
try:
    arguments = int([x.strip() for x in " ".join(arguments[1:]).split(",")][0])
except:
    print("You need to use an integer.")
    arguments = 0

data_retrieval.get_data()

# Two-letter words
for x in onsets:
    if x == "z": x = "ž"
    for a in vowels:
        new_word = x + a
        if new_word == "ži": new_word = "že"
        gen_words[2].append(new_word)
for a in vowels:
    for y in codas:
        new_word = a + y
        gen_words[2].append(new_word)

# Three-letter words (CVC)
for x in onsets:
    if x == "z": x = "ž"
    for a in vowels:
        for y in codas:
            if x + a == "ži":
                new_word = "že" + y
            else:
                new_word = x + a + y
            gen_words[3].append(new_word)

# Three-letter words (VCV)
for a in vowels:
    for y in codas:
        for z in vowels:
            if z == "e" and y in fricatives:
                new_word = a + y + "ë"
            elif y == "z" and z == "i":
                new_word = a + y + "ë"
            else:
                new_word = a + y + z
            gen_words[3].append(new_word)

# Four-letter words (CVC-V)
for x in onsets:
    if x == "z": x = "ž"
    for a in vowels:
        for y in codas:
            for z in vowels:
                if z == "e" and y in fricatives:
                    new_word = x + a + y + "ë"
                gen_words[4].append(new_word)
# Four-letter words (CV-CV)
for x in onsets:
    if x == "z": x = "ž"
    for a in vowels:
        for y in onsets:
            for z in vowels:
                if z == "e" and y in fricatives:
                    new_word = x + a + y + "ë"
                elif x in fricatives and y in ejectives and a == "e":
                    new_word = x + "ë" + y + z
                gen_words[4].append(new_word)

# Four-letter words (V-CVC)
for a in vowels:
    for y in onsets:
        for z in vowels:
            if y + z == "zi": z = "e"
            for x in codas:
                if z == "e" and y in fricatives:
                    new_word = a + y + "ë" + x
                elif y in ejectives and a == "e":
                    gen_words[4].append("ë" + y + z + x)
                    new_word = a + y + z + x
                else:
                    new_word = a + y + z + x
                gen_words[4].append(new_word)

with open("materials/data.tsv", "r") as f:
    for line in f: # add words for lookahead purposes
        l = line.split('\t')
        if l[1] != "—" and l[1] != "Type":
            dict_words.append(l[0])
    totalWords = len(dict_words)

for a in range(2,5):
    for x in gen_words[a][:]:
        if x in dict_words:
            gen_words[a].remove(x)
    gen_words[a] = list(dict.fromkeys(gen_words[a]))
    print(f"\n{a}-letter words:")
    words = []
    dupes = 0
    for x in range(arguments):
        word = random.choice(gen_words[a])
        if word in words:
            dupes += 1
        else:
            print(word)
        words.append(word)
    print(f"({dupes} duplicate{'' if dupes == 1 else 's'} removed)")