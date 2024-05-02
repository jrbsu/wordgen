from modules import utils

def adjective_table(current_word):
    adj_table = "{| class='wikitable'\n|+[[Severan:Adjectives|Inflection]] of ''" + current_word + "''\n!{{gender|solar|adj}}\n!{{gender|lunar|adj}}\n|-\n"
    solar_adj = utils.stress(current_word, current_word + "lo")
    lunar_adj = utils.stress(current_word, current_word + "te")
    adj_table += "|" + solar_adj + "\n|" + lunar_adj + "\n|-\n"
    adj_table += "|}\n"
    return adj_table