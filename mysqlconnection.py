import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        print("init")
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='root',
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection = connection
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # executable = cursor.execute(query, data)
                executable = cursor.execute(query, data)
                # use matching to find if find()
                print("Running this query", executable)
                # if query[0:6].lower() == 'select':
                if query.lower().find("insert") >= 0:
                    self.connection.commit()
                    cursor.close()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()
                    cursor.close()
                    return result
                # elif query[0:6].lower() == 'insert':
                else:
                    self.connection.commit()
                    cursor.close()
           
            except Exception as e:
                print("Something went wrong", e)
                return False
            finally:
                self.connection.close()
    

def connectToMySQL(db):
    return MySQLConnection(db)