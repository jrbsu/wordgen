import re, csv

from modules import definitions

def boolean(s):
    return s.lower() == "true"

def capitalise(definition):
    acronyms = ["e.g.", "i.e.", "lit."]
    capitalise_dict = {}
    for index, acronym in enumerate(acronyms):
        capitalise_dict[acronym] = "acr" + str(index)
    capitalise_dict_inv = {v: k for k, v in capitalise_dict.items()}
    definition = multiple_replace(capitalise_dict, definition)
    definition = re.sub(r'\.$','',definition.capitalize())
    definition = '. '.join(list(map(lambda x: x.strip().capitalize(), definition.split('. '))))
    definition = multiple_replace(capitalise_dict_inv, definition)
    output = f"# {definition}.\n"
    return output

def multiple_replace(dict, text):
    # Create a regular expression  from the dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

def quick_mode():
    done_words = []
    with open("dict.txt") as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(r"^'''(.*?)'''$", line)
            if match:
                done_words.append(match.group(1))
    with open("data.tsv", "r") as f:
        reader = csv.reader(f, delimiter="\t")
        data = [row for row in reader if row[0] not in done_words]
    with open("quick-data.tsv", "w") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(data)

# Dedupe:
# This will find and eliminate illegal clusters (usually two vowels in a row) and log output to `logs/errorlog.txt`.
def dedupe(c, e):
    letterInsert = "j"
    letterRegex = r'\g<1>' + letterInsert + r'\g<2>'
    new_word = e
    # Conversions
    new_word = re.sub(r'tt', r'4', new_word)
    new_word = re.sub(r'kk', r'5', new_word)
    new_word = re.sub(r'i([aeioë])', r'j\g<1>', new_word)
    new_word = re.sub(r'([a-z])\1\1?', r'\g<1>', new_word)
    if len(e) <= 4:
        # letter between two vowels
        new_word = re.sub(r'([aeioë])([aeioë])', letterRegex, new_word)
    else:
        new_word = re.sub(r'([aeioë])([aeioë])', r'\g<1>', new_word)
    new_word = re.sub(r'([eëoi])an$', r'\g<1>n', new_word)
    # Handling <c> and <x>
    new_word = re.sub(r'ket([xc])', r"ke\g<1>", new_word) # for "ket"
    # future forms
    #new_word = re.sub(r'([ptkbdg])([xc])', r"\g<1>'", new_word) # for plosives
    #new_word = re.sub(r'([xc])[xc]', r"\g<1>'", new_word) # for two in a row
    #new_word = re.sub(r'([xczs])(x)(\w?)$',r"\g<1>'\g<3>", new_word)

    new_word = re.sub(r'([mnptkbdg])ë', r'\g<1>e', new_word)
    new_word = re.sub(r'4', r'tt', new_word)
    new_word = re.sub(r'5', r'kk', new_word)
    # if e != new_word:
    #     dupeOutput += c + ": "
    #     dupeOutput += "Had to convert " + e + " to " + new_word + "\n"
    return new_word

#Syllable finder
def stress(current_word, word, list_needed=False):
    word = dedupe(current_word, word)
    syllableList = []
    holding = re.sub(r'(f|v|s|z|c|x|l|j|r|ž)e', r'\g<1>ë', multiple_replace(definitions.diphthong_dict_inv, word))
    letters = list(re.sub(r'[\s\?]', '', holding))
    current_string = letters[0]
    for index, letter in enumerate(letters):
        if index != 0: # First letter is always included
            try:
                nextLetter = letters[index + 1]
            except:
                nextLetter = "b"
            try:
                lastLetter = letters[index - 1]
            except:
                lastLetter = "b"

            if re.search(r'[123]', letter):
                current_string += letter
            elif len(current_string) < 3 and (re.search(r'[cdfgklnrstxzaioeë45]', letter) and re.search(r'[bcdfgjklmnprstvwxz45]', nextLetter) and not re.search(r'[123]', lastLetter)):
                current_string += letter
            elif len(current_string) < 2 and (re.search(r'j', letter) and re.search(r'[aeioë]', nextLetter)):
                current_string += letter
            elif len(current_string) < 3 and re.search(r'[123]', lastLetter) and re.search(r'[aeioë]', letter):
                syllableList.append(current_string)
                current_string = str(letter)
            elif len(current_string) == 3 and re.search(r'.j[eëi]', current_string):
                current_string += letter
            else:
                syllableList.append(current_string)
                current_string = str(letter)
    syllableList.append(current_string)

    stressed_syllable = stress_finder(syllableList)

    syllableList[stressed_syllable] = re.sub(r'(v|s|z|c|x|f|l|j|r|ž)ë', r'\g<1>e', syllableList[stressed_syllable])

    for c, a in enumerate(syllableList):
        syllableList[c] = multiple_replace(definitions.diphthong_dict, a)
        
    if list_needed:
        return syllableList
    else:
        return "".join(syllableList)

def stress_finder(syllables):
    stressed_syllable = 0
    for count, x in enumerate(syllables):
        if re.search(r'(tt|kk|4|5)', x):
            stressed_syllable = count
    return stressed_syllable

# IPA generation
def ipa_gen(current_word, is_syllables=False):
    if not is_syllables:
        syllables = stress(current_word, current_word, True)
    else:
        syllables = current_word
    IPAList = []
    for count, syllable in enumerate(syllables):
        IPAInput = multiple_replace(definitions.diphthong_dict_inv, syllable)
        IPAInput = multiple_replace(definitions.ipa_dict, IPAInput)
        IPAInput = re.sub(r'-', '', IPAInput) # handles suffixes
        IPAList.append(IPAInput)
    if len(IPAList) > 1:
        stressed_syllable = stress_finder(syllables)
        IPAList[stressed_syllable] = "ˈ" + IPAList[stressed_syllable]
        if count != stressed_syllable and re.search(r'(v|s|z|c|x|f|l|j|r|ž)i', syllable):
            IPAList[count] = re.sub(r'(v|s|ʒ|ç|ʝ|f|l|j|r|ʃ)i', r'\g<1>ɪ', IPAList[count])
    return IPAList

def redirects(no_redirect, current_word):
    out = ""
    sans_e = re.sub(r'ë', 'e', current_word)
    if sans_e != current_word and re.search(r'^ž', current_word) and current_word not in no_redirect:
        out += "{{-start-}}\n'''" + re.sub(r'^ž', "z", sans_e) + "'''\n#REDIRECT[[" + current_word + "]]\n[[Category:Redirects handling ⟨ë⟩]][[Category:Redirects handling ⟨ž⟩]]{{-stop-}}\n"
    elif re.search(r'^ž', current_word):
        out += "{{-start-}}\n'''" + re.sub(r'^ž', "z", current_word) + "'''\n#REDIRECT[[" + current_word + "]]\n[[Category:Redirects handling ⟨ž⟩]]{{-stop-}}\n"
    elif sans_e != current_word and current_word not in no_redirect:
        out += "{{-start-}}\n'''" + sans_e + "'''\n#REDIRECT[[" + current_word + "]]\n[[Category:Redirects handling ⟨ë⟩]]{{-stop-}}\n"
    return out

def glyphs(current_word):
    glyphs_code = re.sub(r'ž', 'zh', re.sub(r'ë', 'y', re.sub(r'tt', 'b', re.sub(r'kk', 'p', current_word))))
    return f"{{{{glyphs|{glyphs_code}}}}}\n"