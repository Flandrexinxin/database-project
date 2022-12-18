# 数据库功能函数
import pymysql
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector
import string
import random
import pymysql,csv,pandas
import datetime as dt

#连接数据库
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

#关闭数据库
def close_db(conn):
    # close link
    conn.close()
    return

def get_user_tuple(account):
    conn = get_db()
    db = conn.cursor()

    sql = 'select * from staff where account=%s'# % (account)
    db.execute(sql,(account,))
    ret = db.fetchall()

    db.close()
    close_db(conn)

    return ret

# add staff infomation into database
def add_staff(new_account,staff_type,account_name,street=None):
  if(len(new_account)!=len(account_name)):
    return 'lenth is not illegal'
  conn=get_db()
  cursor=conn.cursor(prepared=True)
  if street==None:
    for i in range(len(new_account)):
      se_password=generate_password_hash(new_account[i][1])
      sql='insert into staff(account,password,type,street,name) values(%s,%s,%s,%s,%s)'
      cursor.execute(sql,(new_account[i][0],se_password,staff_type,None,account_name[i]))
      conn.commit()
  else:
    for i in range(len(new_account)):
      se_password=generate_password_hash(new_account[i][1])
      sql='insert into staff(account,password,type,street,name) values(%s,%s,%s,%s,%s)'
      cursor.execute(sql,(new_account[i][0],se_password,staff_type,street[i],account_name[i]))
      conn.commit()

  cursor.close()
  close_db(conn)
  return

# create the number of amount accounts and passwords
def create_password(amount):  
    new_account = []
    for i in range(amount):
        account = ''.join(random.sample(string.digits, 8))
        password = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        new_account.append((account, password))
    return new_account

# check whether account is in database and correct
def check_account(account, password):  
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor

    sql = 'select * from staff where account=%s' #% (account)
    db.execute(sql,(account,))
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

#录入函数
#核酸检测信息表
def single_insert_na_test_results(id,test_time,result,test_id):
    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into NA_test_results(ID,test_time,result,test_ID) values(%s,%s,%s,%s)'
    cursor.execute(sql, (id, test_time, result, test_id))
    conn.commit()

    cursor.close()
    close_db(conn)
    return

def csv_insert_na_test_results(path):
    df=pandas.read_csv(path,encoding='utf-8')
    values=df.values.tolist()

    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into NA_test_results(ID,test_time,result,test_ID) values(%s,%s,%s,%s)'

    for i in values:
        cursor.execute(sql,(i[0],i[1],i[2],i[3]))
        conn.commit()

    cursor.close()
    close_db(conn)
    return

#场所扫码信息表
def single_insert_Scan_code_info(place_id,id,enter_time):
    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Scan_code_info(Place_ID,ID,enter_time) values(%s,%s,%s)'
    cursor.execute(sql, (place_id,id,enter_time))
    conn.commit()

    cursor.close()
    close_db(conn)
    return

def csv_insert_Scan_code_info(path):
    df=pandas.read_csv(path,encoding='utf-8')
    values=df.values.tolist()

    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Scan_code_info(Place_ID,ID,enter_time) values(%s,%s,%s)'

    for i in values:
        cursor.execute(sql,(i[0],i[1],i[2]))
        conn.commit()

    cursor.close()
    close_db(conn)
    return

#居民居住信息表
def single_insert_Residence_info(id,name,tele_number,sex,birthday,community,enter_date,out_date):
    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Residence_info(ID,name,tele_number,sex,birthday,community,enter_date,out_date)' \
          ' values(%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(sql, (id,name,tele_number,sex,birthday,community,enter_date,out_date))

    conn.commit()

    cursor.close()
    close_db(conn)
    return

def csv_insert_Residence_info(path):
    df=pandas.read_csv(path,encoding='utf-8')
    values=df.values.tolist()

    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Residence_info(ID,name,tele_number,sex,birthday,community,enter_date,out_date)' \
          ' values(%s,%s,%s,%s,%s,%s,%s,%s)'

    for i in values:
        cursor.execute(sql,(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
        conn.commit()

    cursor.close()
    close_db(conn)
    return

#小区/场所信息表
def single_insert_Location_info(name,place_id,street,manager,tele_number):
    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Location_info(name,Place_ID,street,manager,tele_number) values(%s,%s,%s,%s,%s)'
    cursor.execute(sql, (name,place_id,street,manager,tele_number))
    conn.commit()

    cursor.close()
    close_db(conn)
    return

def csv_insert_Location_info(path):
    df=pandas.read_csv(path,encoding='utf-8')
    values=df.values.tolist()

    conn = get_db()
    cursor = conn.cursor()
    sql = 'insert into Location_info(name,Place_ID,street,manager,tele_number) values(%s,%s,%s,%s,%s)'

    for i in values:
        cursor.execute(sql,(i[0],i[1],i[2],i[3],i[4]))
        conn.commit()

    cursor.close()
    close_db(conn)
    return

#查询函数
#查询所给街道内的阳性病例
def get_ill_info_street(street):
    #输入街道的名字，输出一个包含多个元组的列表，每个元组依次包含的内容（）
    conn=get_db()
    cursor=conn.cursor()

    sql="""select * from Residence_info
           where community in (select name from Location_info
           where street=%s)
           and ID in(select ID from NA_test_results where result='阳性')
           """#%(street)
    cursor.execute(sql,(street,))
    ret=cursor.fetchall()
    cursor.close()
    close_db(conn)
    return ret

#查询时间范围内的阳性病例
def get_ill_info_time(begin_time,end_time):
    conn = get_db()
    cursor = conn.cursor()

    sql = """select * from Residence_info
             where ID in(
             select ID from NA_test_results
               where result='阳性' and test_time>=%s and test_time<=%s)
               """# % (begin_time,end_time)
    cursor.execute(sql,(begin_time,end_time))
    ret = cursor.fetchall()
    cursor.close()
    close_db(conn)
    return ret

#通过姓名查找
def get_resident_info_name(name):
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor

    sql = 'select * from Residence_info where name=%s' #% (name)
    db.execute(sql,(name,))
    ret = db.fetchall()  # get the result

    db.close()
    close_db(conn)

    return ret

#通过身份证号查找
def get_resident_info_identity(id):
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor

    sql = 'select * from Residence_info where id=%s'# % (id)
    db.execute(sql,(id,))
    ret = db.fetchall()  # get the result
    
    db.close()
    close_db(conn)

    return ret

#按所在街道查询阳性病例
def get_resident_info_region(region,rtype):
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor
    if rtype=='community':
        sql = 'select * from Residence_info where community=%s' #% (region)
    else:
        sql='select x.ID,x.name,x.tele_number,sex,birthday,community,enter_date,out_date from Residence_info x,Location_info y where y.street=%s and x.community=y.name'#%(region)
    
    db.execute(sql,(region,))
    ret = db.fetchall()  # get the result
    
    db.close()
    close_db(conn)

    return ret

#检查核酸结果格式是否正确
def medical_check(pID,datetime,result,tID):
    if len(pID)==18 and (result=='阴性' or result=='阳性') and len(tID)==10 and pID.isdecimal()==True and tID.isdecimal()==True:
        try:
            dt.datetime.strptime(datetime,"%Y-%m-%d %H:%M")
            return True
        except ValueError:
            return False
    else:
        return False

#检查核酸结果格式是否正确
def medical_check_csv(pID,datetime,result,tID):
    if len(pID)==18 and (result=='阴性' or result=='阳性') and len(tID)==10 and pID.isdecimal()==True and tID.isdecimal()==True:
        try:
            dt.datetime.strptime(datetime,"%Y/%m/%d %H:%M")
            return True
        except ValueError:
            return False
        # return True
    else:
        return False

#检查核酸检测结果是否录入
def medical_typein(pID,date_time,result,sample_num):
    conn = get_db()
    cursor = conn.cursor()

    sql = 'select * from NA_test_results where test_ID=%s'#%(sample_num)
    cursor.execute(sql,(sample_num,))
    ret = cursor.fetchall()
    if len(ret)!=0:
        cursor.close()
        close_db(conn)
        return False
    else:
        single_insert_na_test_results(pID,date_time,result,sample_num)
        cursor.close()
        close_db(conn)
        return True

#覆盖原核酸结果信息
def medical_cover(pID,date_time,result,sample_num):
    conn = get_db()
    cursor = conn.cursor(prepared=True)

    sql = 'delete from NA_test_results where test_ID=%s'#%(sample_num)  #删除原先的

    cursor.execute(sql,(sample_num,))
    conn.commit()
    #ret = cursor.fetchall()
    cursor.close()
    close_db(conn)

    single_insert_na_test_results(pID,date_time,result,sample_num)#重新插入
    return

#给定阳性病例身份证号和时间段，查询在该时间段内与给定病例到达过同一场所的居民信息
def get_close_location(id,begin_time,end_time):
    #输出一个列表，其中每一项为一个元组，元组中包含居民信息
    conn = get_db()
    cursor = conn.cursor()

    sql = """select * from Residence_info
             where ID in( select scan1.ID from Scan_code_info scan1
             where scan1.Place_ID in(  
             select scan2.Place_ID
             from Scan_code_info scan2
             where scan2.ID=%s and scan2.enter_time>=%s and scan2.enter_time<=%s)
             and scan1.enter_time>=%s and scan1.enter_time<=%s)
             """ #% (id,begin_time,end_time,begin_time,end_time)
    cursor.execute(sql,(id,begin_time,end_time,begin_time,end_time))
    ret = cursor.fetchall()
    cursor.close()
    close_db(conn)
    return ret

#输入检测编号，查找前后七天内的密接
def get_close_region(test_id):
    conn = get_db()  # Connecting to the Database
    db = conn.cursor()  # get the cursor

    sql = """select distinct x1.ID,name,tele_number,sex,birthday,community,enter_date,out_date
            from Residence_info x1,NA_test_results y1
            where y1.test_ID=%s
		    and x1.community in (select distinct r1.community
							    from Residence_info r1,NA_test_results tt
							    where tt.test_ID=y1.test_ID and r1.ID=tt.ID and (r1.enter_date<=tt.test_time+7
							    or r1.out_date>=tt.test_time-7 or (r1.out_date=null and r1.enter_date<=tt.test_time+7)))
		    and (x1.out_date+7>=y1.test_time or x1.enter_date-7<=y1.test_time
            or (x1.out_date=null and x1.enter_date<=y1.test_time+7))""" #% (test_id)
    db.execute(sql,(test_id,))
    ret = db.fetchall()  # get the result
    
    db.close()
    close_db(conn)

    return ret

def medical_if_exists(test_id):
    conn = get_db()
    cursor = conn.cursor()

    sql = 'select * from NA_test_results where test_ID=%s'#%(test_id)
    cursor.execute(sql,(test_id,))
    ret = cursor.fetchall()
    if len(ret)!=0:
        cursor.close()
        close_db(conn) 
        return True
    cursor.close()
    close_db(conn) 
    return False

def get_user_name(the_account):
    conn = get_db()  # Connecting to the Database
    cursor = conn.cursor()  # get the cursor
    sql = 'select name from staff where account=%s'#%(the_account)
    cursor.execute(sql,(the_account,))
    ret = cursor.fetchall()
    cursor.close()
    close_db(conn) 
    return ret

def delete_user(the_account):
    conn = get_db()  # Connecting to the Database
    cursor = conn.cursor()  # get the cursor
    for item in the_account:
        print(item)
        sql = 'delete from staff where account=%s'#%(item)
        cursor.execute(sql,(item,))
        conn.commit()
    cursor.close()
    close_db(conn)      

def check_resident_info(pid,name,phone,sex,birth,street,come_date,leave_date):
    if len(pid)== 18 and len(name)<=10 and len(phone)==11 and (sex=='男' or sex=='女') and len(street)<21:
        return True
    else:
        return False 

def change_password(account,new_pwd):
  if new_pwd.isdigit()==False and new_pwd.isalpha()==False:
    conn = get_db() # Connecting to the Database
    db = conn.cursor() # get the cursor

    se_pwd=generate_password_hash(new_pwd)
    sql = 'update staff set password=%s where account=%s'
    db.execute(sql,(se_pwd,account))
    conn.commit()

    db.close()
    close_db(conn)

    return True
  else:
    return False

def get_account_street(account_name):
    conn = get_db()  # Connecting to the Database
    cursor = conn.cursor()  # get the cursor
    sql = 'select street from staff where account=%s'#%(account_name)
    cursor.execute(sql,(account_name,))
    ret = cursor.fetchall()
    cursor.close()
    close_db(conn) 
    return ret

def check_if_place_id_in(place_id):
    conn = get_db()  # Connecting to the Database
    cursor = conn.cursor()  # get the cursor
    sql = 'select count(*) from Location_info where Place_ID=%s'#%(place_id)
    cursor.execute(sql,(place_id,))
    ret = cursor.fetchall()
    cursor.close()
    close_db(conn) 
    if ret != 0:
        return True
    else:
        return False