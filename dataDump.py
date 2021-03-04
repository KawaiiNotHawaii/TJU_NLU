# this file will RE-WRITE table novels and output_novels, and clear table guesses
#do set AUTO_INCREMENT TO 0 before running this script to re-dumping the data

import json
import pymysql

data = []

for path in ('data/dev.json', 'data/test.json'):
    with open(path) as f:
        for line in f:
            json_obj = json.loads(line)
            del json_obj['gpt_out']
            del json_obj['ppl']
            context=""
            for c_text in json_obj['c']:
                context += c_text.replace(" ", "")
            tup = (context, json_obj['t'].replace(" ", ""), json_obj['words'].replace(" ", ""))
            data.append(tup)

print("{} records to be dump".format(len(data)))
with open("./hosts.json", 'r') as f:
    info = json.loads(f.readline())
f.close()
conn = pymysql.connect(host=info['host'], port=info['port'],
                            user=info['user'], password=info['password'], db=info['db'])
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

query = "INSERT INTO novels (context, target_sentence, target_word) VALUES (%s, %s, %s)"
cursor.executemany(query, data)
conn.commit()
conn.close()
print("all settled and ready to go;")
