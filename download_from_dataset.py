from databaseConn import MySqlHelper
import pymysql
import hosts
import json
#pymysql = MySqlHelper()
host = hosts.Hosts()

conn = pymysql.connect(host=host.host, port=host.port,
                            user=host.user, password=host.password, db=host.db)
cursor = conn.cursor()
query = "SELECT * FROM guesses"
cursor.execute(query)
guesses = cursor.fetchall()
query = "SELECT * FROM novels"
cursor.execute(query)
novels = cursor.fetchall()
f = open('shibiao/with_context_step2.json', 'w', encoding='utf-8')
for guess_raw, novel_raw in zip(guesses, novels):
    _,_,_,guess,t_words, is_right = guess_raw
    _,novel_id, context, target_sentence,_,_,_,_ = novel_raw
    example = {
        'novel_id': novel_id,
        'context': context,
        'target_sentence': target_sentence,
        't_words': t_words,
        'guess': guess,
        'is_right': is_right
    }
    f.write(json.dumps(example, ensure_ascii=False) + '\n')
f.close()
