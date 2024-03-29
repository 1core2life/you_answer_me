import pymysql


class Database():

    def __init__(self, dbName):
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='',
                                  db=dbName,
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)


    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        return self.cursor.lastrowid

    
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    
    def commit(self):
        self.db.commit()

