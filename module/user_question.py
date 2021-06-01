from module import DBModule


class UserQuestion:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select(self, user_idx):
        sql = "select * from user_question where user_idx = %s "        
        row = self.db_class.executeAll(sql,(user_idx))
        
        return row


    def is_correct(self, user_idx, question_idx, answer):
        sql = "select * from user_question where user_idx = %s and question_idx = %s and answer = %s "        
        row = self.db_class.executeOne(sql,(user_idx, question_idx, answer))
        
        if row:
            return True
        else:
            return False


    def insert(self, question_idx, user_idx, answer):
        sql = "INSERT INTO user_question(question_idx, user_idx, answer) VALUES(%s, %s, %s)"

        self.db_class.execute(sql, (question_idx, user_idx, answer))
        self.db_class.commit()
        

    