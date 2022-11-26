# 数据库功能函数
import pymysql
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import string
import random

def get_db():
    #connect database
    conn = mysql.connector.connect(
        host='43.138.62.72',  #IP
        port=6666,
        user='root',
        password='123456',
        db='six_crew',
        #charset='utf8',
        auth_plugin='mysql_native_password'
    )
    return conn  #establish link

def close_db(conn):
    # close link
    conn.close()
    return

def add_staff(new_account,staff_type,street='NULL'):#add staff infomation into database
    conn=get_db()
    cursor=conn.cursor(prepared=True)
    for i in range(len(new_account)):
        se_password=generate_password_hash(new_account[i][1])
        sql='insert into staff(account,password,type,street) values(%s,%s,%s,%s)'
        cursor.execute(sql,(new_account[i][0],se_password,staff_type,street))
        conn.commit()

    cursor.close()
    close_db(conn)
    return

def create_password(amount):  # create the number of amount accounts and passwords
    new_account = []
    for i in range(amount):
        account = ''.join(random.sample(string.digits, 8))
        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_account.append((account, password))
    return new_account


def check_account(account, password):  # check whether account is in database and correct
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor

    sql = 'select * from staff where account="%s"' % (account)
    db.execute(sql)
    ret = db.fetchall()  # get the result

    db.close()  # close cursor
    close_db(conn)  # close database
    #print(ret)
    if len(ret) == 0:  # no account
        return "Not Exists"
    else:
        if check_password_hash(ret[0][1], password) == True:  # correct password
            return ret[0][2]
        else:  # incorrect password
            return "wrong"
