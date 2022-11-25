# 数据库功能函数
import pymysql
def get_db():
    #connect database
    conn = pymysql.connect(
        host='43.138.62.72',  #IP
        port=6666,
        user='root',
        password='123456',
        db='six_crew',
        charset='utf8'
    )
    return conn  #establish link

def close_db(conn):
    # close link
    conn.close()
    return
