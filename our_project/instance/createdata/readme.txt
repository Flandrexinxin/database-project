createdata.py为生成数据库中数据的程序
community_info.csv为北京市部分小区及其所属街道的信息，也是生成数据库中数据必要的初始数据，请在运行程序时将该文件与py文件放在一个文件夹中
程序中所用到的列表和子函数功能具体见程序中的注释
使用方法：
依次调用函数：
create_info()
insert_community()
insert_community_ID()
insert_name_phone()
程序运行完成后，会生成7个csv文件：
out.csv
out2.csv
out3.csv
residence_info.csv
scan_info.csv
test_result.csv
test_result2.csv

其中，out.csv为最终的居民居住信息，可直接插入Residence_info表中
out2.csv为最终的扫码信息，可直接插入Scan_code_info表中
out3.csv为最终的场所信息，可直接插入Location_info表中
test_result.csv为最终的核酸检测结果信息，可直接传入NA_test_results表中

