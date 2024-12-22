gajra_letters = ["c", "d", "g", "k", "l", "n", "r", "s", "t", "x", "z"]
diphthong_dict = {
    "1": "aj",
    "2": "ij",
    "3": "oj",
    "4": "tt",
    "5": "kk",
}
diphthong_dict_inv = {v: k for k, v in diphthong_dict.items()}
ipa_dict = {
    "c": "ç",
    "e": "ɛ",
    "ë": "ə",
    "g": "ɟ",
    "ï": "ɪ",
    "k": "c",
    "o": "ʌ",
    "x": "ʝ",
    "z": "ʃ",
    "ž": "ʒ",
    "1": "eɪ",
    "2": "aɪ",
    "3": "ʌɪ",
    "4": "tʼ",
    "5": "cʼ",
}
type_dict = {
    "adj.": "Adjective",
    "adv.": "Adverb",
    "conj.": "Conjuction",
    "det.": "Determiner",
    "excl.": "Exclamation",
    "mod.": "Modifier",
    "n.": "Noun",
    "part.": "Particle",
    "prep.": "Adposition",
    "pron.": "Pronoun",
    "suff.": "Suffix",
    "v.": "Verb"
}
mood_dict = {
    # "type": ["suffix", "meaning", needs_mutation?]
    "normal": ["", "", False],
    "negative": ["an", "not, NEG", True],
    "abilitive": ["tti", "to be able to, ABL", False],
    "optative": ["kki", "to want to, OPT", False],
    "dubitative": ["do", "might, DUB", True],
    "conditional": ["sa", "would; depends upon another condition, COND", True],
    "questioning": ["ko", "questioning, QUES", True],
    "deonotic": ["afi", "should, DEO", False]
}

persons = ["1S", "1P", "2", "3S", "3P", "FORM"]
tenses = ["present", "habitual", "past", "future"]

gajra_ends = {
    "present": {"1S": "", "1P": "er", "2": "ad", "3S": "as", "3P": "ilan", "FORM": "ket"},
    "habitual": {"1S": "ne", "1P": "nera", "2": "na", "3S": "anes", "3P": "inen", "FORM": "ket"},
    "past": {"1S": "rë", "1P": "era", "2": "ra", "3S": "arës", "3P": "irën", "FORM": "etrë"},
    "future": {"1S": "", "1P": "", "2": "", "3S": "", "3P": "", "FORM": ""}
}

non_gajra_ends = {
    "present": {"1S": "i", "1P": "er", "2": "ad", "3S": "as", "3P": "ilan", "FORM": "eket"},
    "habitual": {"1S": "ene", "1P": "enera", "2": "ana", "3S": "anes", "3P": "inen", "FORM": "eket"},
    "past": {"1S": "erë", "1P": "era", "2": "ara", "3S": "arës", "3P": "irën", "FORM": "etrë"},
    "future": {"1S": "o", "1P": "o", "2": "o", "3S": "o", "3P": "o", "FORM": "o"}
}

verb_begins = {
    "future": {"1S": "e", "1P": "era", "2": "da", "3S": "la", "3P": "lan", "FORM": "ket"}
}

verb_begins_vowel = {
    "future": {"1S": "en", "1P": "eran", "2": "dan", "3S": "lan", "3P": "lan", "FORM": "ket"}
}

row_name_data = {
    "BASE": "",
    "POSS_1S": "1st person",
    "POSS_2S": "2nd person",
    "POSS_3S": "3rd person",
    "POSS_1P": "1st person",
    "POSS_2P": "2nd person",
    "POSS_3P": "3rd person",
    "CASE_GEN": "genitive",
    "CASE_INE": "inessive",
    "CASE_ADE": "adessive",
    "CASE_ABL": "ablative",
    "CASE_ALL": "allative",
    "CASE_INSTR": "instrumental",
    "NUM_NONE": "none",
    "NUM_SING": "singular",
    "NUM_DUAL": "dual",
    "NUM_PLU": "plural",
    "NUM_PAU": "paucal",
    "NUM_COLL": "collective",
}
