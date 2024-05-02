import requests
from bs4 import BeautifulSoup
import argparse
import re

parser = argparse.ArgumentParser(description="Gets words that need to be deleted",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-l", "--local", action="store_true", help="use a local html dump of the base words page `base_words.html`")
args = vars(parser.parse_args())
local = args["local"]

def convert(word):
    word = re.sub(r'\\xc3\\xab', 'ë', word)
    word = re.sub(r'\\xc5\\xbe', 'ž', word)
    return word

def get_words():
    words = []
    if local:
        with open("base_words.html") as f:
            page = "\n".join(f.readlines())
        soup = BeautifulSoup(str(page), "html.parser")
    else:
        URL = "https://wiki.joesutherland.rocks/index.php/Severan:Base_words"
        page = requests.get(URL)
        soup = BeautifulSoup(str(page.content), "html.parser")
    div = soup.find('div', attrs={'class': 'div-col'})
    for link in div.find_all('a'):
        words.append(convert(link.text.strip()))
    print(f"Got {len(words)} words from the 'Base words' page.")
    return words

def load_base_words(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        words = f.readlines()
        for word in words:
            word = convert(word)
    return words

def add_category(word):
    out = "{{-start-}}\n"
    out += f"'''{word}'''\n[[Category:Words no longer in the spreadsheet]]\n"
    out += "{{-stop-}}\n"
    return out

def load_spreadsheet_words():
    params = {
        'gid': '1317019602',
        'single': 'true',
        'output': 'tsv',
    }
    response = requests.get(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vRfi01S0PTVSeFRSLdW2z8azjhdxUAn1B5hmoPFCwDwshwHGzXHdYWog-TPzYNlblurk-kWM3BXfwKD/pub',
        params=params,
    )
    response.encoding = response.apparent_encoding
    content = str(response.text)
    content = content.split("\n")

    words = []

    for line in content:
        items = line.split("\t")
        word = items[0]
        word_type = items[1]
        if word_type not in ["—", "Type"]:
            words.append(word)
    
    words_len = len(list(dict.fromkeys(words)))

    print(f"Got {words_len} unique words from the spreadsheet.")

    return words

def main():
    # base_words = load_base_words('base-words.txt')
    base_words = get_words()
    spreadsheet_words = load_spreadsheet_words()
    
    out = ""
    number = 0
    for word in base_words:
        if word.strip() not in spreadsheet_words:
            out += add_category(word.strip())
            number += 1

    f = open("materials/words_to_delete.txt", "w")
    f.write(out)
    if number == 0:
        print("Spreadsheet and page are synced.")
    else:
        print(f"Written {number} words to `materials/words_to_delete.txt`.")
    f.close()

if __name__ == '__main__':
    main()
