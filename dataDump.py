# this file will RE-WRITE table novels and output_novels, and clear table guesses
#do set AUTO_INCREMENT TO 0 before running this script to re-dumping the data

import json
import pymysql

data = []

for path in ('test_dev/dev.json', 'test_dev/test.json'):
    with open(path) as f:
        for line in f:
            json_obj = json.loads(line)
            del json_obj['gpt_out']
            del json_obj['ppl']
            tup = (json_obj['c'][0].replace(" ", ""), json_obj['t'].replace(" ", ""), json_obj['words'].replace(" ", ""))
            data.append(tup)

print("{} records to be dump".format(len(data)))

conn = pymysql.connect(host="rm-2ze3ya354780fhb70fm.mysql.rds.aliyuncs.com", port=3306,
                            user="tjunlu", password="Tjunlu123", db="chinese_novel")
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

