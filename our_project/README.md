# 实施过程实时更新
## 文件介绍
* auth.py主要写了登录视图，由刘鑫和蹇倩完成
* CDC.py, street.py, medical.py分别是是疾控中心工作人员模块，街道管理人员模块，医务工作者模块，各自有有主页、各功能页面等视图，由刘鑫和蹇倩完成
* 在templas文件夹中，是各个页面对应的html文件，由陶然完成
* db.py文件封装了数据库操作相关的功能函数，由后端小组完成
## 前端
### html文件(To Tr)
* /CDC/main页面：有四个代表四项功能的图标，点击后分别跳转到相应页面，有用户的基本信息，
* To Tr：关于页面的搭建
CDC/inquire：这个页面实现疾控中心工作人员对居民信息的查询。在提交表单后，需要返回查询结果，结果以表格形式展示，表格中的数据将会以列表形式传给html，同时还会返回一个名为length的参数，表示列表的长度，即表格除了表头的行数
不同类型数据传输至html的相关操作可以参考链接：https://blog.csdn.net/qq_48736958/article/details/107949098

### 明确搭建哪些页面？（完善慕客）
* 登陆页面，如果登陆失败，做出相应提示，如：“用户名不存在”、“密码错误”
* 街道管理人员功能页面，列出四项功能（见前文需求分析），点击后跳转至相应页面
* 医务人员功能页面，列出修改/录入/删除核酸检测结果的功能，点击后跳转至相应页面
* 疾控中心工作人员功能页面，列出四项功能（见前文需求分析），点击后跳转至相应页面
* 录入/修改页面1：录入居住于该街道的居民个人信息以及进出当前居住地的时间
* 录入页面2：场所码扫码结果录入
* 录入页面3：录入该街道的小区/场所相关信息
* 查询页面1：通过身份证号、姓名等信息查找该街道居民的信息
* 录入/修改页面4：通过核酸样本编号录入结果，若查询到该样本编号对应的数据已存在，则向用户确认是否覆盖，是就update，否就取消操作。
* 查询页面2：通过姓名、身份证号等查找居民信息，或者浏览某一区域的情况
* 查询页面3：按照时间范围或所在的相关街道，查询阳性病例
* 查询页面4：输入病例的检测编号，根据其居住地排 查检测时间前后7天的密接人群
* 查询页面5：输入病例的身份证号以及排查的时间范围，查询与该病例在指定时间范围内密接的人员

##后端
### 后端实现的功能函数
#### 基础函数
* get_db()：连接数据库，返回一个与数据库建立的链接。
* close_db(conn):断开与数据库的连接，输入以上建立的链接，无返回值。
* get_user_tuple(account)：根据账号返回用户信息

#### 超级管理员函数
* add_staff(new_account,staff_type,account_name,street='NULL')：将管理人员信息传入数据库中，依次输入管理员信息列表，管理员类型（类型包括：super manager,medical staff,street manager,CDC staff），姓名（是一个列表，长度与new_account相同），所管理的街道（默认为NULL）；无返回值
* create_password(amount)：创建规定数量的管理人员账号和密码，输入要创建的数量，输出一个包含若干元组的列表，每个元组包含账号、密码。
* check_account(account,password)：检查输入的账号密码是否正确匹配，输入要登录的账号和密码，当输入账号错误时，输出"Not Exists"；当输入账号正确，密码错误时，输出"wrong"；当输入账号密码均正确时，输出管理员类型的字符串（类型包括：super manager,medical staff,street manager,CDC staff）

#### 查询函数
* get_ill_info_street(street)：查询所给街道的阳性病例，输入街道的名字，返回一个包含n个元组的列表，每个元组包含一条居民信息。
* get_ill_info_time(begin_time,end_time)：查询在给定时间范围（输入时间类型为年月日时分，例"2022-08-09 20:50"）内检测出阳性的病例的居民信息，输入开始时间和截止时间，返回一个包含n个元组的列表，每个元组包含一条居民信息。
* get_resident_info_name(name)：通过姓名查找居民信息。返回结果同上。
* get_resident_info_identity(identity)：通过身份证号查找居民信息。返回结果同上。
* get_resident_info_region(region,rtype)：查找某一区域的全部居民信息，region为街道或者小区名称，rtype为region的类型(street,community)，street为街道，community为小区。返回结果同上。
* get_close_location(id,begin_time,end_time)：给定阳性病例身份证号和时间段，查询在该时间段内与给定病例到达过同一场所的居民信息，输入阳性病例身份证号和一个时间范围（年月日时分，例"2022-06-04 13:42"），返回一个包含n个元组的列表，每个元组包含一条居民信息。
* get_close_region(test_id)：输入阳性病例的检测编号，查询在病例检测时间前后7天内，与病例在同一街道/小区居住的人员。返回结果同上。

#### 其他功能函数
* medical_check(pID,datetime,result,tID)：检查核酸检测结果格式是否正确。正确返回True，否则返回False。正确示例：（'206711200412231678', '2022-09-19 17:34:00', '阳性', '1761533951'）。pID长度为11的char型，result长度为4的char型("阳性","阴性")，tID长度为10的char型。
* medical_typein(pID,date_time,result,sample_num)：核酸检测结果录入，输入身份证号、检测时间、检测结果、检测编号，返回True表示录入成功，返回False表示输入的检测号表中已存在。
* medical_cover(pID,date_time,result,sample_num)：检测号原本已经在表中存在的情况下，覆盖该行数据，输入身份证号、检测时间、检测结果、检测编号，无返回。

#### 插入函数
* single_insert_na_test_results(id,test_time,result,test_id)：插入单条核酸检测结果信息
* single_insert_Scan_code_info(place_id,id,enter_time)：插入单条场所码扫码信息
* single_insert_Residence_info(id,name,tele_number,sex,birthday,community,enter_date,out_date)：插入单条居民居住信息
* single_insert_Location_info(name,place_id,street,manager,tele_number)：插入单条小区/场所信息
* csv_insert_na_test_results(path)：从csv中批量导入核酸检测结果信息。path为csv文件的存储路径。
* csv_insert_Scan_code_info(path)：从csv中批量导入场所码扫码信息。path为csv文件的存储路径。
* csv_insert_Residence_info(path)：从csv中批量导入居民居住信息。path为csv文件的存储路径。
* csv_insert_Location_info(path)：从csv中批量导入小区/场所信息。path为csv文件的存储路径。

#### 表结构
* table NA_test_results( //核酸检测结果信息表 3NF
    ID char(18) NOT NULL, //居民身份证号，char型，18位
    test_time datetime NOT NULL,//检测时间，时分秒，datetime型，精确到秒
    result char(4),//检测结果，char型，阴性,阳性
    test_ID char(10) PRIMARY KEY//检测样本编号，char型，8位                         
)

table Scan_code_info( //场所码扫码信息表 1NF
    Place_ID char(4) NOT NULL,//场所编码，char型，
    ID char(18) NOT NULL,//居民身份证号，char型，18位
    enter_time datetime NOT NULL//进入时间，时分秒，datetime型，精确到秒
)

table Residence_info(  //居民居住信息表 1NF
    ID char(18) NOT NULL,//居民身份证号，char型，18位
    name varchar(10), //姓名，varchar型，最长10位
    tele_number char(11) NOT NULL, //联系方式，char型，11位
    sex char(2), //性别，char型，男,女
    birthday date,//出生年月日，date型，精确到日
    community varchar(20) NOT NULL,//所在小区，varchar型，最长20位
    enter_date date NOT NULL,//进入当前居住地日期，date型，精确到日
    out_date date//离开当前居住地日期，date型，精确到日
)

table Location_info( //小区/场所信息表 3NF
    name varchar(20) NOT NULL,//名称，varchar型，最长20位
    Place_ID char(4) PRIMARY KEY,//场所编码，char型，
    street varchar(20) NOT NULL,//所在街道，varchar型，最长20位
    manager varchar(10) NOT NULL,//负责人姓名，varchar型，最长10位
    tele_number char(11) NOT NULL//联系方式，char型，11位 
)

table staff(//用户表 3NF
    account char(8) PRIMARY KEY,//账号，char型，
    password varchar(200) NOT NULL,//密码，varchar型，
    type varchar(50),//人员类型，super manager,medical staff,street manager,CDC staff
    street varchar(20),//所在街道，街道管理人员此属性有值，其他人员类型为空值
    name varchar(20)//用户名
)