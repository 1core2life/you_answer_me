from module import DBModule


class Question:
    def __init__(self):
        self.db_class = DBModule.Database("USER")

    def select_all(self):
        sql = "select * from question"        
        row = self.db_class.executeAll(sql)
        
        return row

    def select(self, idx):
        sql = "select * from question where idx = %s "        
        row = self.db_class.executeOne(sql,(idx))
        
        return row


    def insert(self, content):
        sql = "INSERT INTO question(content) VALUES(%s)"

        idx = self.db_class.execute(sql, (content))
        self.db_class.commit()

        return idx
        

    def update(self, idx, content):
        sql = "UPDATE question set content = %s where idx = %s"

        self.db_class.execute(sql, (content, idx))
        self.db_class.commit()
        

    def get_max_length(self):
        sql = "SELECT COUNT(*)  as cnt FROM question"        
        row = self.db_class.executeOne(sql)
        
        return row

    