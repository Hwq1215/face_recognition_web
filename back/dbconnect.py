import mysql.connector

import config

db = mysql.connector.connect(
    host=config.dbinfo()['host'],
    user=config.dbinfo()['username'],
    passwd=config.dbinfo()['password'],
    database=config.dbinfo()['database'] 
)
_cursor = db.cursor()

def insert(sql,val):
    _cursor.execute(sql,val)
    db.commit()

def insert_all(sql,val):
    _cursor.executemany(sql,val)
    db.commit()

def select(sql):
    _cursor.execute(sql)
    return _cursor.fetchall()

def test():
    print(_cursor.execute('select * from face_info'))
    
