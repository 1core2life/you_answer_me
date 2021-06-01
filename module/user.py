from module import DBModule
from random import randint
import random
import string


class User:
    def __init__(self):
        self.db_class = DBModule.Database("USER")


    def select(self, user_idx):
        sql = "select * from user where idx = %s "        
        row = self.db_class.executeOne(sql,(user_idx))
        
        return row

    def select_code(self, code):
        sql = "select * from user where code = %s "        
        row = self.db_class.executeOne(sql,(code))
        
        return row


    def is_already_code(self, code):
        sql = "select * from user where code = %s"        
        row = self.db_class.executeOne(sql,(code))

        if row:
            return True
        else:
            return False


    def insert(self, name):
        code = self.getRandomCode()
        sql = "INSERT INTO user(name, code) VALUES(%s, %s)"

        user_idx = self.db_class.execute(sql, (name, code))
        self.db_class.commit()

        return user_idx


    def getRandomCode(self):
        while(True):
            code = str()
            
            for index in range(0,6):
                intOrString = randint(0, 2)
                if intOrString == 0:
                    code = code + random.choice(string.ascii_letters)
                else:
                    code = code + str(randint(1, 9))
            
            row = self.is_already_code(code)

            if not row:
                return code
        
        
            

    