import mysql.connector

import config

class mysqlConnect:
    def __init__(self,db=None,_cursor=None):
        self.db = db
        self._cursor = _cursor
    def __enter__(self):
        self.db = mysql.connector.connect(
            host=config.dbinfo()['host'],
            user=config.dbinfo()['username'],
            passwd=config.dbinfo()['password'],
            database=config.dbinfo()['database'] 
        )
        self._cursor = self.db.cursor()
        return (self._cursor,self.db)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if(self._cursor is not None):
            self._cursor.close()
        if(self.db is not None):
            self.db.close()


# return mysqlConnect()
def connect()->mysqlConnect:
    return mysqlConnect()

def connectStart():
    db = mysql.connector.connect(
        host=config.dbinfo()['host'],
        user=config.dbinfo()['username'],
        passwd=config.dbinfo()['password'],
        database=config.dbinfo()['database'] 
    )
    _cursor = db.cursor()
    return _cursor,db

def connectEnd(cursor,db):
    cursor.close()
    db.close()


def insert(sql,val):
    with mysqlConnect() as (_cursor,db):
        _cursor.execute(sql,val)
        db.commit()

def insert_all(sql,val):
    with mysqlConnect() as (_cursor,db):
        _cursor.executemany(sql,val)
        db.commit()

def select(sql):
    with mysqlConnect() as (_cursor,db):
        _cursor.execute(sql)
        res = _cursor.fetchall()
    return res


def select_param(sql,val):
    with mysqlConnect() as (_cursor,db):
        _cursor.execute(sql,val)
        res = _cursor.fetchall()
    return res


# def test():
#     print(_cursor.execute('select * from face_info'))
    
