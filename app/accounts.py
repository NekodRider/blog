import pymysql
from flask import flash
config_ac = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'passwd',
    'db': 'accounts',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
config_art = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'passwd',
    'db': 'articles',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
config_cmt = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'passwd',
    'db': 'comments',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
def login_Check(id,pw):
    connection = pymysql.connect(**config_ac)
    c = connection.cursor()
    if id!="":
        sql="select * from account where id='"+id+"'"
        c.execute(sql)
        results=c.fetchall()
        if not results:
            connection.close()
            return False
        elif results[0]['password']==pw:
            connection.close()
            return results[0]
    else:
        connection.close()
        return False

def Register(id,name,pw):
    connection = pymysql.connect(**config_ac)
    c = connection.cursor()
    if id!="" and name!="" and pw!="":
        sql="select * from account where id='"+id+"'"
        c.execute(sql)
        results=c.fetchall()
        if not results:
            sql="insert into account values('"+id+"','"+name+"','"+pw+"')"
            c.execute(sql)
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return 1
    else:
        connection.close()
        return 2

def Post(name,content):
    connection = pymysql.connect(**config_art)
    c = connection.cursor()
    if name!="":
        sql="select * from article where name='"+name+"'"
        c.execute(sql)
        results=c.fetchall()
        if not results:
            sql="insert into article values('"+name+"','"+content+"')"
            c.execute(sql)
            connection.commit()
            connection.close()

            return True
        else:
            connection.close()
            return False
    else:
        connection.close()
        return False

def delete_Post(name):
    connection = pymysql.connect(**config_art)
    c = connection.cursor()
    if name!="":
        sql="delete from article where name='"+name+"'"
        c.execute(sql)
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False

def getComment(art_name):
    connection = pymysql.connect(**config_cmt)
    c = connection.cursor()
    sql = "select name, content from comment where art_name='"+art_name+"'"
    c.execute(sql)
    results =c.fetchall()
    connection.close()
    return results

def Comment(art_name,name,content):
    connection = pymysql.connect(**config_cmt)
    c = connection.cursor()
    sql="insert into comment values('"+art_name+"','"+content+"','"+name+"')"
    c.execute(sql)
    connection.commit()
    connection.close()
    return True

def getPost():
    connection = pymysql.connect(**config_art)
    c = connection.cursor()
    sql = "select name, content from article"
    c.execute(sql)
    results =c.fetchall()
    connection.close()
    return results

def Edit(name,content):
    connection = pymysql.connect(**config_art)
    c = connection.cursor()
    if name!="":
        sql="select * from article where name='"+name+"'"
        c.execute(sql)
        results=c.fetchall()
        if results:
            sql="update article set content='"+content+"' where name='"+name+"'"
            c.execute(sql)
            connection.commit()
            connection.close()

            return True
        else:
            connection.close()
            return False
    else:
        connection.close()
        return False
