from modules import definitions, utils
import re

def replace_e(word):
    return re.sub(r'ë([sn]?)$', r'e\g<1>', word)

def check_gajra(verb):
    new_verb = re.sub(r'[iëe]$', "", verb)
    if re.search(r'[aeëio](n|d|g|t|k|s|z|c|x|l|r|n|d|g|t|k|s|z|c|x|l|r|(aj|ij|oj))$', new_verb) and len(new_verb) > 1:
        is_gajra = True
    else:
        is_gajra = False
    return is_gajra

def verb_table(verb_type, verb, current_word):
    generated_words = []
    gerunds = []
    verb_table = ""
    if definitions.mood_dict[verb_type][2] == True:
        is_gajra = check_gajra(current_word)
    else:
        is_gajra = check_gajra(current_word + definitions.mood_dict[verb_type][0])

    suffix, tooltip_text, mutation = definitions.mood_dict[verb_type]
    if verb_type != "normal": 
        tooltip = f"{{{{tooltip£{verb_type}£{tooltip_text}}}}}"

    verb = re.sub(r'(v|s|z|c|x|w|l|j|r|ž)e', r'\g<1>ë', verb)

    if not mutation:
        verb = re.sub(r'ë$', 'e', verb) + suffix

    if verb_type == "normal":
        verb_table += f"{{| class='wikitable'\n|+Inflection of ''{utils.stress(current_word, verb)}'' (normal form)\n!tense\n!{{{{tooltip|1S|1st-person singular}}}}\n!{{{{tooltip|1P|1st-person plural}}}}\n!{{{{tooltip|2|2nd-person singular/plural}}}}\n!{{{{tooltip|3S|3rd-person singular}}}}\n!{{{{tooltip|3P|3rd-person plural}}}}\n!{{{{tooltip|FORM|formal}}}}\n|-\n"
    elif mutation:
        verb_table += f"{{| class='wikitable'\n|+Inflection of ''{utils.stress(current_word, re.sub(r'ë$', 'e', verb) + suffix)}'' ({tooltip} form)\n!tense\n!1S\n!1P\n!2\n!3S\n!3P\n!FORM\n|-\n"
    else:
        verb_table += f"{{| class='wikitable'\n|+Inflection of ''{utils.stress(current_word, verb)}'' ({tooltip} form)\n!tense\n!1S\n!1P\n!2\n!3S\n!3P\n!FORM\n|-\n"

    # Remove the final <i>
    new_verb = re.sub(r'[iëe]$', "", verb)

    # if re.search(r'(f|v|s|z|c|x|l|j|r)$', new_verb) and len(new_verb) > 1:
    #     gajra_ends[1] = "ër"
    #     non_gajra_ends[1] = "ër"

    # TODO: These probably need to be moved down
    # Check if the verb begins with a vowel
    if re.match(r'^[aeioë]', new_verb):
        begins = definitions.verb_begins_vowel
    else:
        begins = definitions.verb_begins

    # Check if the final letter is "z"
    if re.search(r'z$', new_verb) and len(new_verb) > 1:
        definitions.non_gajra_ends["present"]["1S"] = "ë"
    else:
        definitions.non_gajra_ends["present"]["1S"] = "i"

    # If the verb ending is gajra...
    if is_gajra:
        # Add an "i" if the ending is disallowed word-finally
        if re.search(r'([bcdfgjklmnpqrstvxzž])([bcdfgjklmnpqrstvxzž])$', new_verb):
            new_verb = re.sub(r'([bcdfgjklmnpqrstvxzž])([bcdfgjklmnpqrstvxzž])$', r'\g<1>\g<2>i', new_verb)
        endings = definitions.gajra_ends
    else:
        endings = definitions.non_gajra_ends

    # Check if the first letter is "t"
    if re.search(r'^t', new_verb):
        begins["future"]["FORM"] = "ke"
    else:
        begins["future"]["FORM"] = "ket"

    for tense in definitions.tenses:
        verb_table += f"!{tense}\n"
        for person in definitions.persons:
            if tense != "future":
                if not mutation:
                    verb_table += f"|[[{utils.stress(current_word, replace_e(new_verb) + endings[tense][person])}]]\n"
                    generated_words.append(utils.stress(current_word, replace_e(new_verb) + endings[tense][person]))
                else:
                    verb_table += f"|[[{utils.stress(current_word, replace_e(new_verb + endings[tense][person]) + suffix)}]]\n"
                    generated_words.append(utils.stress(current_word, replace_e(new_verb + endings[tense][person]) + suffix))
            if tense == "future":
                if mutation:
                    verb_table += f"|[[{utils.stress(current_word, begins[tense][person] + replace_e(re.sub(r'ž', 'z', new_verb) + endings[tense][person]) + suffix)}]]\n"
                    generated_words.append(utils.stress(current_word, begins[tense][person] + replace_e(re.sub(r'ž', 'z', new_verb) + endings[tense][person]) + suffix))
                else: # FUT, mutation type
                    verb_table += f"|[[{utils.stress(current_word, begins[tense][person] + replace_e(re.sub(r'ž', 'z', new_verb) + endings[tense][person]))}]]\n"
                    generated_words.append(utils.stress(current_word, begins[tense][person] + replace_e(re.sub(r'ž', 'z', new_verb) + endings[tense][person])))
        verb_table += "|-\n"
    
    if verb_type == "normal":
        gerund = utils.stress(current_word, replace_e(current_word + "ma"))
        verb_table += f"|-\n!gerund\n|colspan=7|[[{gerund}]]\n"
        generated_words.append(gerund)
        # FIXME: remove this probably
        gerunds.append(f"{gerund}\tg.\tgerund form of ''[[{current_word}]]''.\t{current_word}")

    verb_table += "|}\n"
    return verb_table, generated_words, gerunds