import pymysql.cursors

class Database:

    __connection = None

    @classmethod
    def get_connection(cls):
        if cls.__connection == None:
            cls.__connection=pymysql.connect(host='localhost',
                user='islam',
                password='iti',
                db='ChatGame',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
        return cls.__connection
