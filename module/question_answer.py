from module import DBModule


class QuestionAnswer:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select(self, question_idx):
        sql = "select * from question_answer where question_idx = %s "        
        row = self.db_class.executeAll(sql,(question_idx))
        
        return row


    def update(self, idx, content):
        sql = "UPDATE question_answer set content = %s where question_idx = %s"

        self.db_class.execute(sql, (content, idx))
        self.db_class.commit()


    def insert(self, question_idx, content):
        sql = "INSERT INTO question_answer(question_idx, content) VALUES(%s, %s)"

        self.db_class.execute(sql, (question_idx, content))
        self.db_class.commit()
        

    