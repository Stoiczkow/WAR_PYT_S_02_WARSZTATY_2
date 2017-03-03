from models.crypto import *

class User(object):
    __id = None
    name = None
    __hashed_password = None
    email = None
    
    def __init__(self):
        self.__id = -1
        self.name = ""
        self.email = ""
        self.__hashed_password = ""
        
    @property
    def id(self):
        return self.__id
    
    @property
    def hashed_password(self):
        return self.__hashed_password
    
    def set_password(self, password):
        self.__hashed_password = password_hash(password)
        
    def save_to_db(self, cursor, cnx):
        if self.__id == -1:
            sql = """INSERT INTO User(name, hashed_password, email)
            VALUES('{}', '{}', '{}')
            """.format(self.name, self.__hashed_password, self.email)
            cursor.execute(sql)
            cnx.commit()
            self.__id = cursor.lastrowid
            return True
        else:
            return False
    
    @staticmethod
    def load_user_by_id(cursor, id):
        sql = "SELECT id, name, email, hashed_password FROM User WHERE id='{}'".format(id)
        result = cursor.execute(sql)
        data = cursor.fetchone()
        if data is not None:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.name = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, name, email, hashed_password FROM User"
        ret = []
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.name = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret
