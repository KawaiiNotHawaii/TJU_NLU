import json
import pymysql
import hosts
import random
random.seed(123456)


data = []
nums = 0
file_names = ['./datas/dev_final.json', './datas/test_final.json']
for path in file_names:
    with open(path, encoding='utf-8') as f:
        for line in f:
            json_obj = json.loads(line)
            context=""
            for c_text in json_obj['context']:
                context += c_text.replace(" ", "")
            choices_text = []

            #print(choice_text)
            #print(index_text)
            #print(choice_list)
            #print(choice_index_list)
            #print(json_obj['novel_id'])
            tup = (int(json_obj['novel_id']), context, json_obj['target_sentence'].replace(" ", ""), json_obj['target_words'].replace(" ", ""), \
                   json_obj['extra'], json_obj['tag'])
            data.append(tup)
random.shuffle(data)
data = data[:1000]
datas = []
max_users = 3
nums_users = 3
per_users = int(len(data) / nums_users) + 1
for i in range(nums_users):
    datas.append(data[i* per_users : (i+1) * per_users])



print("{} records to be dump".format(len(data)))
host = hosts.Hosts()

for user_id in range(max_users):
    conn = pymysql.connect(host=host.host, port=host.port,
                                user=host.user, password=host.password, db=host.db)
    cursor = conn.cursor()

    clear_guesses = "DELETE FROM {}".format("guesses{}".format(user_id+1))
    cursor.execute(clear_guesses)
    print("guesses cleared;")
    clear_output_novels = "DELETE FROM {}".format("output_novels{}".format(user_id+1))
    cursor.execute(clear_output_novels)
    print("output_novels cleared;")
    clear_novels = "DELETE FROM {}".format("novels{}".format(user_id+1))
    cursor.execute(clear_novels)
    print("novels cleared;")
    reset_auto_increment = "ALTER TABLE {} AUTO_INCREMENT=0".format("novels{}".format(user_id+1))
    cursor.execute(reset_auto_increment)
    print("AUTO_INCREMENT reset;")
    '''
    query = "INSERT INTO novels (novel_id, context, target_sentence, target_word, extra, tag) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(query, data)
    '''
    conn.commit()
    conn.close()



for idx, data in enumerate(datas[:nums_users]):
    conn = pymysql.connect(host=host.host, port=host.port,
                                user=host.user, password=host.password, db=host.db)
    cursor = conn.cursor()

    query = "INSERT INTO {} (id, context, target_sentence, target_word, extra, tag) VALUES (%s, %s, %s, %s, %s, %s)".format("novels{}".format(idx+1))
    cursor.executemany(query, data)
    conn.commit()
    conn.close()
