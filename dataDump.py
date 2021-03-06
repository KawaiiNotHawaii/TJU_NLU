# this file will RE-WRITE table novels and output_novels, and clear table guesses
#do set AUTO_INCREMENT TO 0 before running this script to re-dumping the data

import json
import pymysql
import hosts
import random
random.seed(123456)

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

class Choies(object):
    def __init__(self, choice, is_real):
        self.choice = choice
        self.is_real = str(is_real)



data = []

for path in ('data/dev_not_context.json', 'data/test_not_context.json'):
    tag = path.split('/')[-1].split('.')[0]
    nums = 0
    with open(path, encoding='utf-8') as f:
        for line in f:
            choiess = []
            json_obj = json.loads(line)

            context=""
            for c_text in json_obj['c']:
                context += c_text.replace(" ", "")
            choiess.append(Choies(json_obj['words'], 1))
            choices_text = []
            for choice in json_obj['gpt_ft_out']:
                choice = choice.replace('[UNK]', '')
                c_context = ''
                for c in choice:
                    if is_all_chinese(c):
                        continue
                    c_context += c
                if c_context != '':
                    choices_text.append(c_context)
            choices_text = list(set(choices_text))
            for c_context in choices_text:
                choiess.append(Choies(c_context, 0))
            if len(choiess) == 1:
                #print(json_obj['gpt_ft_out'])
                nums += 1
            ##assert len(choiess) > 1
            random.shuffle(choiess)
            choice_list = []
            choice_index_list = []
            for choice in choiess:
                choice_list.append(choice.choice)
                choice_index_list.append(choice.is_real)
            choice_text = ' '.join(choice_list)
            index_text = ' '.join(choice_index_list)
            #print(choice_text)
            #print(index_text)
            #print(choice_list)
            #print(choice_index_list)
            #print(json_obj['novel_id'])
            tup = (int(json_obj['novel_id']), context, json_obj['t'].replace(" ", ""), json_obj['words'].replace(" ", ""), tag, choice_text, index_text)
            data.append(tup)
random.shuffle(data)
data = data[:150]



print("{} records to be dump".format(len(data)))
host = hosts.Hosts()

conn = pymysql.connect(host=host.host, port=host.port,
                            user=host.user, password=host.password, db=host.db)
cursor = conn.cursor()

clear_guesses = "DELETE FROM guesses"
cursor.execute(clear_guesses)
print("guesses cleared;")
clear_output_novels = "DELETE FROM output_novels"
cursor.execute(clear_output_novels)
print("output_novels cleared;")
clear_novels = "DELETE FROM novels"
cursor.execute(clear_novels)
print("novels cleared;")
reset_auto_increment = "ALTER TABLE novels AUTO_INCREMENT=0"
cursor.execute(reset_auto_increment)
print("AUTO_INCREMENT reset;")

query = "INSERT INTO novels (novel_id, context, target_sentence, target_word, tag, choice, choice_index) VALUES (%s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(query, data)

conn.commit()
conn.close()
print("all settled and ready to go;")

