from module import DBModule


class Challenger:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select_all(self, user_idx):
        sql = "select * from challenger where user_idx = %s "        
        row = self.db_class.executeAll(sql,(user_idx))
        
        return row

    
    def insert_comment(self, user_idx, challenger_idx, comment):
        sql = "UPDATE challenger set comment = %s where user_idx = %s and challenger_idx = %s"

        self.db_class.execute(sql, (comment, user_idx, challenger_idx))
        self.db_class.commit()



    def insert(self, user_idx, name, score):
        sql = "INSERT INTO challenger(user_idx, name, score) VALUES(%s, %s, %s)"

        idx = self.db_class.execute(sql, (user_idx, name, score))
        self.db_class.commit()

        return idx
        

    