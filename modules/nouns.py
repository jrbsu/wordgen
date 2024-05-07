from modules import utils, definitions
import re

row_data = {
    "BASE": [],
    "POSS_1S": [],
    "POSS_2S": [],
    "POSS_3S": [],
    "POSS_1P": [],
    "POSS_2P": [],
    "POSS_3P": [],
    "CASE_GEN": [],
    "CASE_INE": [],
    "CASE_ADE": [],
    "CASE_ABL": [],
    "CASE_ALL": [],
    "CASE_INSTR": [],
    "NUM_NONE": [],
    "NUM_SING": [],
    "NUM_DUAL": [],
    "NUM_PLU": [],
    "NUM_PAU": [],
    "NUM_COLL": [],
}

case_dict = {
    "erg": 0,
    "acc": 1,
    "dat": 2,
    "abs": 3
}

def make_row(case_name, bold=False, colspan=None, tooltip=None):
    out = ""
    words = row_data[case_name]
    text = definitions.row_name_data[case_name]
    if tooltip is not None:
        text = f"{{{{tooltip|{text}|{tooltip}}}}}"
    if colspan is not None:
        out += f"! colspan='{colspan}' |{text}\n"
    elif case_name != "BASE":
        out += f"! {text}\n"
    erg, acc, dat, abs = words
    if bold:
        row = f"|'''[[{erg}]]'''\n|'''[[{acc}]]'''\n|'''[[{dat}]]'''\n|'''[[{abs}]]'''\n|-\n"
    else:
        row = f"|[[{erg}]]\n|[[{acc}]]\n|[[{dat}]]\n|[[{abs}]]\n|-\n"
    out += row
    return out

def new_line():
    return "|-\n"

def class_number(rowspan, number):
    return f"! rowspan='{rowspan}' |{number}\n" if rowspan != 1 else f"! {number}\n"

def top_class(rowspan, text):
    return f"! rowspan='{rowspan}' |{text}\n"

def noun_with_suffix(current_word, base_words, suffix):
    erg, acc, dat, abs = base_words
    return [
        utils.stress(current_word, re.sub(r'ë$', 'e', erg) + suffix),
        utils.stress(current_word, re.sub(r'ë$', 'e', acc) + suffix),
        utils.stress(current_word, re.sub(r'ë$', 'e', dat) + suffix),
        utils.stress(current_word, re.sub(r'ë$', 'e', abs) + suffix)
    ]

# Noun table function
def get_noun_data(current_word, gender, is_special):
    noun_gajra = True
    if letter_match := re.search(r'(.$)', current_word, re.IGNORECASE):
        noun_end = letter_match.group(1)
    if letter_match2 := re.search(r'(.).$', current_word, re.IGNORECASE):
        second_last = letter_match2.group(1)
    else:
        second_last = "none"
    letter_match_two_const = re.search(r'(..).$', current_word, re.IGNORECASE)
    if letter_match_two_const:
        last_two = letter_match_two_const.group(1)
        if re.search(r'[bcdgjklmnprstvwxz][bcdgjklmnprstvwxz]', last_two):
            noun_gajra = False

    # Ergative
    erg = current_word

    # Accusative
    acc = current_word
    if gender == "solar":
        if re.search(r'[aio]', noun_end):
            if re.search(r'[fvszcxwljr]', second_last):
                acc = re.sub(r'[aio]$', 'ë', current_word)
            else:
                acc = re.sub(r'[aio]$', 'e', current_word)
        elif re.search(r'[eë]', noun_end):
            acc = re.sub(r'[eë]$', 'o', current_word)
        else:
            if re.search(r'[fvszcxwljr]', second_last) or re.search(r'[fvszcxwljr]', noun_end):
                acc = current_word + "ë"
            else:
                acc = current_word + "e"
    if gender == "lunar":
        if len(current_word) <= 2 or noun_gajra == False:
            acc = current_word + "jë"
        elif re.search(r'[aio]', noun_end):
            acc = re.sub(r'[aio]$', 'jë', current_word)
        elif re.search(r'[eë]', noun_end):
            acc = re.sub(r'[eë]$', 'ja', current_word)
        else:
            acc = current_word + "jë"
    if is_special and re.search(r'[aioeë]', noun_end):
        acc = current_word + "s" # HACK
    elif is_special:
        acc = current_word + "es" # HACK

    # Dative
    dat = current_word
    if re.search(r'[io]', noun_end):
        if len(current_word) > 2 or noun_gajra == True:
            dat = re.sub(r'[io]$', 'ë', current_word)
        else:
            dat = dat + "xë"
    elif re.search(r'[eë]', noun_end):
        if len(current_word) > 2 or noun_gajra == True:
            dat = re.sub(r'[eë]$', 'o', current_word)
        else:
            dat = dat + "xo"
    else:
        dat = current_word + "a"
    if re.search(r'([bjmpvw])(x\w?)$', dat):
        morph += f"(Also had to add an 'a')"
        dat = re.sub(r'([bjmpvw])(x\w?)$',r'\g<1>a\g<2>', dat)

    # Absolutive
    abs = current_word
    if gender == "lunar":
        if re.search(r'[aeëio]', noun_end):
            abs = current_word + "t"
        else:
            abs = current_word + "at"
    elif gender == "solar":
        if re.search(r'[aeëio]', noun_end):
            abs = current_word + "l"
        else:
            abs = current_word + "al"

    erg = utils.stress(current_word, erg)
    abs = utils.stress(current_word, abs)
    if len(acc) <= 2 and gender != "solar":
        acc = utils.stress(current_word, re.sub(r'ë$', 'e', acc))
        dat = utils.stress(current_word, re.sub(r'ë$', 'e', dat))
    else:
        acc = utils.stress(current_word, acc)
        dat = utils.stress(current_word, dat)

    base_words = [erg, acc, dat, abs]
    row_data["BASE"] = base_words

    # specialWords hack:
    if is_special:
        acc = utils.stress(current_word, acc + "ë")

    # POSS 1S
    row_data["POSS_1S"] = [
        utils.stress(current_word, erg + "en"),
        utils.stress(current_word, acc + "n"),
        utils.stress(current_word, dat + "n"),
        utils.stress(current_word, abs + "en")
    ]
    if re.search(r'[aeëio]', noun_end):
        row_data["POSS_1S"][case_dict["erg"]] = utils.stress(current_word, erg + "n")
        if len(acc) <= 2:
            row_data["POSS_1S"][case_dict["acc"]] = utils.stress(current_word, re.sub(r'ë$', 'e', acc) + "n")
        else:
            row_data["POSS_1S"][case_dict["acc"]] = utils.stress(current_word, acc + "n")
        row_data["POSS_1S"][case_dict["dat"]] = utils.stress(current_word, dat + "n")
    elif re.search(r'[fvszcxwljr]', noun_end):
        row_data["POSS_1S"][case_dict["erg"]] = utils.stress(current_word, erg + "ën")
        row_data["POSS_1S"][case_dict["abs"]] = utils.stress(current_word, abs + "ën")
    elif gender == "solar":
        row_data["POSS_1S"][case_dict["abs"]] = utils.stress(current_word, abs + "ën")

    # POSS 2S
    row_data["POSS_2S"] = noun_with_suffix(current_word, base_words, "dan")

    # POSS 3S
    row_data["POSS_3S"] = noun_with_suffix(current_word, base_words, "lan")
    if gender == "solar":
        row_data["POSS_3S"][case_dict["acc"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "an")

    # POSS 1P
    row_data["POSS_1P"] = noun_with_suffix(current_word, base_words, "ran")
    row_data["POSS_1P"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "eran")
    if not re.search(r'[aeëio]', noun_end):
        row_data["POSS_1P"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "eran")

    # POSS 2P
    row_data["POSS_2P"] = noun_with_suffix(current_word, base_words, "danon")

    # POSS 3P
    row_data["POSS_3P"] = noun_with_suffix(current_word, base_words, "lanon")
    if gender == "lunar":
        row_data["POSS_3P"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "anon")

    # CASE_GEN
    row_data["CASE_GEN"] = noun_with_suffix(current_word, base_words, "k")
    if is_special:
        row_data["CASE_GEN"] = noun_with_suffix(current_word, base_words, "ek")
    row_data["CASE_GEN"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ek")
    if not re.search(r'[aeëio]', noun_end):
        row_data["CASE_GEN"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "ek")

    # CASE INE
    row_data["CASE_INE"] = noun_with_suffix(current_word, base_words, "tta")
    row_data["CASE_INE"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "itta")
    if not re.search(r'[aeëio]', noun_end):
        row_data["CASE_INE"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "itta")

    # CASE ADE
    row_data["CASE_ADE"] = noun_with_suffix(current_word, base_words, "jo")

    # CASE ABL
    row_data["CASE_ABL"] = noun_with_suffix(current_word, base_words, "va")

    # CASE ALL
    row_data["CASE_ALL"] = noun_with_suffix(current_word, base_words, "zo")

    # CASE INSTR
    row_data["CASE_INSTR"] = noun_with_suffix(current_word, base_words, "no")
    row_data["CASE_INSTR"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "eno")
    if not re.search(r'[aeëio]', noun_end):
        row_data["CASE_INSTR"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "eno")

    # NUM_NONE
    row_data["NUM_NONE"] = noun_with_suffix(current_word, base_words, "kke")
    row_data["NUM_NONE"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ikke")
    if not re.search(r'[aeëio]', noun_end):
        row_data["NUM_NONE"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "ikke")

    # NUM_SING
    row_data["NUM_SING"] = row_data["BASE"] # Will be the same.

    # NUM_DUAL
    row_data["NUM_DUAL"] = noun_with_suffix(current_word, base_words, "de")
    row_data["NUM_DUAL"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ede")
    if not re.search(r'[aeëio]', noun_end):
        row_data["NUM_DUAL"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "ede")

    # NUM_PLU
    # Might work. Needs testing.
    # row_data["NUM_PLU"] = noun_with_suffix(current_word, base_words, "z")
    # row_data["NUM_PLU"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ez")
    # if not re.search(r'[aeëio]', noun_end):
    #     row_data["NUM_PLU"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "ede")
    
    if re.search(r'[aeëio]', noun_end):
        row_data["NUM_PLU"] = [
            utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "z"),
            utils.stress(current_word, acc + "z"),
            utils.stress(current_word, dat + "z"),
            utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ez")
        ]
    else:
        row_data["NUM_PLU"] = [
            utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "ez"),
            utils.stress(current_word, acc + "z"),
            utils.stress(current_word, dat + "z"),
            utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "ez")
        ]

    # NUM_PAU
    row_data["NUM_PAU"] = noun_with_suffix(current_word, base_words, "rë")
    row_data["NUM_PAU"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "orë")
    if not re.search(r'[aeëio]', noun_end):
        row_data["NUM_PAU"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "orë")

    # NUM_COLL
    row_data["NUM_COLL"] = noun_with_suffix(current_word, base_words, "ca")
    row_data["NUM_COLL"][case_dict["abs"]] = utils.stress(current_word, re.sub(r'ë$', 'e', abs) + "oca")
    if not re.search(r'[aeëio]', noun_end):
        row_data["NUM_COLL"][case_dict["erg"]] = utils.stress(current_word, re.sub(r'ë$', 'e', erg) + "oca")

def noun_table(current_word, gender, is_special):
    get_noun_data(current_word, gender, is_special)
    noun_table = f"{{| class='wikitable'\n|+[[Severan:Nouns|Inflection]] of ''{current_word}''\n! colspan='3' rowspan='2' |role\n!ergative / unmarked\n!accusitive\n!dative\n!absolutive\n|-\n"
    noun_table += make_row("BASE", bold=True)
    noun_table += class_number(6, 2)
    noun_table += top_class(3, "possessive\n(singular)")
    noun_table += make_row("POSS_1S", tooltip="my")
    noun_table += make_row("POSS_2S", tooltip="your")
    noun_table += make_row("POSS_3S", tooltip="his/her/their/its")
    noun_table += top_class(3, "possessive\n(plural)")
    noun_table += make_row("POSS_1P", tooltip="our")
    noun_table += make_row("POSS_2P", tooltip="your")
    noun_table += make_row("POSS_3P", tooltip="their")
    noun_table += class_number(1, 3)
    noun_table += make_row("CASE_GEN", colspan=2)
    noun_table += class_number(5, 4)
    noun_table += make_row("CASE_INE", colspan=2)
    noun_table += make_row("CASE_ADE", colspan=2)
    noun_table += make_row("CASE_ABL", colspan=2)
    noun_table += make_row("CASE_ALL", colspan=2)
    noun_table += make_row("CASE_INSTR", colspan=2)
    noun_table += class_number(6, 5)
    noun_table += top_class(6, "number")
    noun_table += make_row("NUM_NONE")
    noun_table += make_row("NUM_SING")
    noun_table += make_row("NUM_DUAL")
    noun_table += make_row("NUM_PLU")
    noun_table += make_row("NUM_PAU")
    noun_table += make_row("NUM_COLL")
    noun_table += f"|}}\n"
    return noun_table

def generated_words():
    rows = row_data.values()
    generated_words = []
    for row in rows:
        generated_words.extend(row)
    generated_words = list(dict.fromkeys(generated_words))
    return generated_words