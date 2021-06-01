from module import DBModule


class Question:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select(self, idx):
        sql = "select * from question where idx = %s "        
        row = self.db_class.executeOne(sql,(idx))
        
        return row


    def insert(self, content):
        sql = "INSERT INTO question(content) VALUES(%s)"

        idx = self.db_class.execute(sql, (content))
        self.db_class.commit()

        return idx
        

    def get_max_length(self):
        sql = "SELECT COUNT(*)  as cnt FROM question"        
        row = self.db_class.executeOne(sql)
        
        return row

    