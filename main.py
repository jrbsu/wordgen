# Last updated 2024-05-02
import re, progressbar

from modules import args, data_retrieval, definitions, file_management, utils, verbs, nouns, adjectives

words = []
used_words = []
special_words = []
gerunds = []
output = ""
redirects = "" # for pages beginning "ž"
progress = 0
generated_words = []

if args.local:
    print(f"Using local data.")
else:
    data_retrieval.get_data()

with open("materials/data.tsv") as f:
    lines = f.readlines()
    # for line in sorted(lines, key=lambda line: line.split('\t')[0]): # add words for lookahead purposes
    for line in lines:
        l = line.split('\t')
        if l[1] != "—" and len(l[1]) != 0 and l[1] != "Type":
            words.append(l[0])
    print("Found " + str(len(words)) + " rows.")
    total_words = len(words)

# Global vars
morph = ""
is_gajra = False

if args.quick:
    print("Updating only new words (quick mode)")
    utils.quick_mode()
    data_file = "materials/quick-data.tsv"
else:
    data_file = "materials/data.tsv"

with open(data_file) as f:
    print("Generating wikitext...")
    widgets = [
        progressbar.SimpleProgress(), ' ',
        progressbar.Percentage(), ' ',
        progressbar.GranularBar(),
    ]
    with progressbar.ProgressBar(max_value=total_words, widgets=widgets) as bar:
        for i, line in enumerate(f):
            l = line.split('\t')
            current_word = l[0]
            current_part = l[1]
            current_def = l[2].capitalize()
            derived = l[3].strip()
            is_special = utils.boolean(l[4])
            gender = l[5]

            # If part is "—", it's not really a word, so skip.
            if current_part != "—" and current_part != "Type" and current_part != "":
                words.pop(0)

                # Special words.
                if is_special == True:
                    special_words.append(current_word)

                # PRONUNCIATION
                if current_word not in used_words:
                    IPA_code = utils.ipa_gen(current_word)
                    output += "{{-start-}}\n{{lowercase}}\n== Severan ==\n"
                    output += utils.glyphs(current_word)
                    output += f"* IPA: /{''.join(IPA_code)}/\n"
                used_words.append(current_word)

                # WORD TYPE
                category = ""
                try:
                    output += f"==={definitions.type_dict[current_part]}===\n"
                    word_type_cat = definitions.type_dict[current_part].lower()
                    if word_type_cat == "suffix":
                        category += f"[[Category:Severan {word_type_cat}es]]\n"
                    else:
                        category += f"[[Category:Severan {word_type_cat}s]]\n"
                except:
                    output += "===Unknown word type===\n"
                    category += "[[Category:Severan words of unknown type]]\n"
                if is_special:
                    category += "[[Category:Irregular Severan nouns]]\n"

                if derived != "" and derived != "\n" and re.search(r';', derived):
                    derived_list = re.sub(r'; ','|',derived)
                    output += f"{{{{derived|{derived_list}}}}}\n\n"
                elif derived != "" and derived != "\n":
                    output += f"{{{{derived|{derived}}}}}\n\n"

                # Verb table
                if current_part == "v.":
                    verb_tables = []
                    verb_types = definitions.mood_dict.keys()
                    for mood in verb_types:
                        verb_table, word_list, gerund_list = verbs.verb_table(mood, current_word, current_word)
                        verb_tables.append(str(verb_table))
                        generated_words += word_list
                        gerunds += gerund_list
                    if re.search(r'zë$', current_word):
                        category += "[[Category:Severan stative verbs]]\n"

                # Nouns table
                if current_part == "n." or current_part == "pron.":
                    noun_table = nouns.noun_table(current_word, gender, is_special)
                    word_list = nouns.generated_words()
                    generated_words += word_list

                # Adjectives and genders
                if current_part == "adj.":
                    adj_table = adjectives.adjective_table(current_word)

                # Putting it together
                output += f"'''{current_word}'''\n"
                if re.search(r'n\.', current_part):
                    output += f"{{{{gender|{gender}}}}}\n"
                defs_array = []
                if re.search(r';', current_def):
                    defs_array = current_def.split('; ')
                    for definition in defs_array:
                        output += utils.capitalise(definition)
                else:
                    output += utils.capitalise(current_def)
                if current_part == "v.":
                    output += f"{{{{gajra|{'true' if verbs.check_gajra(current_word) else 'false'}}}}}\n"
                    for count, table in enumerate(verb_tables):
                        # For the "normal" table
                        if count == 0:
                            output += table
                        # For all other tables
                        elif count == 1:
                            output += "{{verb forms|1=\n"
                            table = re.sub(r'\|', '{{!}}', table)
                            output += re.sub(r'\£', '|', table)
                        elif count == len(verb_tables) - 1:
                            table = re.sub(r'\|', '{{!}}', table)
                            output += re.sub(r'\£', '|', table)
                            output += "}}\n"
                        else:
                            table = re.sub(r'\|', '{{!}}', table)
                            output += re.sub(r'\£', '|', table)
                if re.search(r'n\.', current_part) or re.search(r'pron\.', current_part):
                    output += noun_table
                if re.search(r'adj\.', current_part):
                    output += adj_table
                if current_word != utils.stress(current_word, False):
                    category += "[[Category:Words with incorrect stress markings]]"
                output += category
                if current_word not in words:
                    output += "{{-stop-}}\n"

                # Handle redirects.
                # Don't overwrite words that actually start with "ë".
                no_redirect = []
                if re.search(r'^ë', current_word):
                    no_redirect.append(current_word)

                redirects += utils.redirects(no_redirect, current_word)

                progress += 1
            bar.update(progress)
        # print("Done {str(progress)} words", end='\r')

file_management.stage(output)

word_list_page = file_management.update_base_words(used_words)

file_management.check_for_update(output, args.force, redirects, word_list_page, generated_words, morph, gerunds)
