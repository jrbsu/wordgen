import filecmp, datetime, re
from modules import backup_management

def update_time(just_time=False):
    now = datetime.datetime.now()
    now_display = now.strftime("%d %B %Y, %X")
    now_iso = now.strftime("%Y-%m-%d-%H-%M-%S")
    update = "{{-start-}}\n'''Template:Last update'''\n" + str(now_display) + "\n{{-stop-}}"
    if just_time == False:
        return update
    else:
        return now_iso

def stage(output):
    f = open("materials/staging.txt", "w")
    f.write(output)
    f.close()

def update(output, redirects, word_list_page, generated_words, morph, gerunds):
    time_update = update_time()
    f = open("materials/dict.txt", "w")
    f.write(output)
    print("Written output to `dict.txt`")
    f = open("materials/updatetime.txt", "w")
    f.write(time_update)
    print("Written timeoutput to `updatetime.txt`")
    f.close()
    backup(output)
    generate_logs(redirects, word_list_page, generated_words, morph, gerunds)

def check_for_update(output, force, redirects, word_list_page, generated_words, morph, gerunds):
    if force:
        print("Written output to `staging.txt`. Force was specified so will update.")
        update(output, redirects, word_list_page, generated_words, morph, gerunds)
    else:
        print("Written output to `staging.txt`. Checking if there was a change...")
        if filecmp.cmp('materials/staging.txt', 'materials/dict.txt') == False:
            print("Change was detected.")
            update(output, redirects, word_list_page, generated_words, morph, gerunds)
        else:
            print("No change was detected.")

def update_base_words(used_words):
    used_words = sorted(used_words)
    word_list_content = []
    for word in used_words:
        if not re.search(r'^-', word):
            word_list_content.append(f"* [[{word}]]\n")
    word_list_content = list(dict.fromkeys(word_list_content))
    word_list_page = "{{-start-}}\n'''Severan:Base words'''\nThis list documents all base words in Severan. There are currently '''" + str(len(word_list_content)) + " words''' in the list, excluding duplicate entries and [[:Category:Severan suffixes|suffixes]].\n{{div col|colwidth=10em}}\n" + "".join(word_list_content) + "{{div col end}}\n{{-stop-}}"
    return word_list_page

def generate_logs(redirects, word_list_page, generated_words, morph, gerunds):
    f = open("materials/redirs.txt", "w")
    f.write(redirects)
    print("Written redirects to `materials/redirs.txt`")
    f.close()

    f = open("materials/base-words.txt", "w")
    f.write(word_list_page)
    print("Written base word list to `materials/base-words.txt`")
    f.close()

    f = open("logs/allwords.txt", "w")
    f.write("All words\n=========\n")
    a = "\n".join(generated_words)
    f.write(a)
    print("Written all words to `logs/allwords.txt`")
    f.close()

    f = open("logs/errorlog.txt", "w")
    # f.write("\nError log\n=============\n")
    # f.write(dupeOutput) FIXME
    f.write("\nMorph log\n========\n")
    f.write(morph)
    print("Written dupes and morphs to `logs/errorlog.txt`")
    f.close()

    f = open("materials/gerunds.txt", "w")
    f.write('\n'.join(gerunds))
    f.close()

def backup(output):
    backup_time = update_time(just_time=True)
    filename = f"backup-{backup_time}.txt"
    f = open(f"logs/backups/{filename}", "w")
    f.write(output)
    print(f"Written a backup to `backup-{backup_time}.txt`")
    f.close()
    backup_management.keep_recent_files('logs/backups')