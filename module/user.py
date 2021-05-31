from module import DBModule


class User:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select(self, idx):
        sql = "select * from user where idx = %s "        
        row = self.db_class.executeOne(sql,(idx))
        
        return row


    def insert(self, name):
        sql = "INSERT INTO user(name) VALUES(%s)"

        user_idx = self.db_class.execute(sql, (name))
        self.db_class.commit()

        return user_idx
        

    