
import pymysql

class MySqlHelper(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host="rm-2ze3ya354780fhb70fm.mysql.rds.aliyuncs.com", port=3306,
                               user="tjunlu", password="Tjunlu123", db="chinese_novel")
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.close()

    def get_num(self, table):
        query = "select count(*) from {}".format(table)
        self.cursor.execute(query)
        data = self.cursor.fetchall()[0][0]
        return data

    def query_by_id(self, id, table):
        try:
            query = "select * from {} where id = {}".format(table, id)
            self.cursor.execute(query)
            data = self.cursor.fetchall()[0]
            return data
        except:
            return None

    # operations for TABLE guesses

    def insert_into_guesses(self, novel_id, user_id, hasContext, guess, isRight):
        try:
            query = """INSERT INTO guesses VALUES ({}, {}, {}, "{}", {})""".format(novel_id, user_id, int(hasContext), guess, int(isRight))
            print("insertion query is:", query)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print("Insertion into guesses failed:", e)
            return "Insertion into guesses failed"

    # operations for TABLE output_novels

    def fetch_randomly(self):
        # randomly fetch a record
        # fetch records to be evaluated with context first, if not exist, fetch records to be evaluated without context
        data = self.select_with_context()
        if (data is not None):
            return (data, True)
        return (self.select_without_context(), False)

    def select_with_context(self):
        # randomly select a record to be evaluated with context
        print("select with context")
        try:
            query = "SELECT * FROM output_novels WHERE hitTimesInContext<2 ORDER BY RAND() LIMIT 1"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            if(id is None):
                return None
            else:
                return self.query_by_id(data[0][0], "novels")
        except Exception as e:
            print("Selection with context failed:", e)
            return "Selection with context failed"

    def select_without_context(self):
        # randomly select a record to be evaluated without context
        print("select without context")
        try:
            # TODO: this query only fetches novels that passed the evaluation with context.
            query = "SELECT * FROM output_novels WHERE hitTimesInContext<2 AND missTimesWithoutContext<10 ORDER BY RAND() LIMIT 1"
            self.cursor.execute(query)
            id = self.cursor.fetchall()[0][0]
            return self.query_by_id(id, "novels")
        except Exception as e:
            print("Selection without context failed:", e)
            return "Selection without context failed"

    def update_times_col(self, novel_id, col):
        try:
            query = "UPDATE output_novels SET {}={}+1 WHERE id={}".format(col, col, novel_id)
            self.cursor.execute(query)
            self.conn.commit();
        except Exception as e:
            print("Updating output_novels failed:", e)
            return "Updating output_novels failed"

    def delete_from_outputNovels(self, novel_id):
        try:
            query = "DELETE FROM output_novels WHERE id={}".format(novel_id)
            self.cursor.execute(query)
            self.conn.commit();
        except Exception as e:
            print("Deleting from contextFilter failed:", e)
            return "Deleting from contextFilter failed"


if __name__ == '__main__':
    tables = "novels"

    sqlh = MySqlHelper()
    sqlh.connect()

    idx = sqlh.query_by_id(1000, tables)
    print(idx)
    idx = sqlh.query_by_id(999, tables)
    print(idx)
    sqlh.disconnect()

#print(d)
