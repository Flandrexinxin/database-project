# ## 街道管理人员蓝图
# #街道管理人员功能页面
# #1、录入居住于该街道的居民个人信息以及进出当前居住地的时间
# #2、记录该街道场所的人员流动信息，即场所码的扫码结果录入 
# #3、录入该街道的小区/场所的相关信息 
# #4、通过姓名、身份证号等查找负责街道的居民信息
# import os
# import csv
# import functools
# from werkzeug.utils import secure_filename
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for
# )
# from project.db import(single_insert_Residence_info,single_insert_Scan_code_info,
#     single_insert_Location_info,get_account_street,get_resident_info_name,get_resident_info_identity
# )

# from project.auth import( login_required )

# bp = Blueprint('street', __name__)

# @bp.route('/streetmain',method = ('GET','POST'))
# @login_required
# def medicalmain():
#     return render_template('street/main.html')

# #1、录入居住于该街道的居民个人信息以及进出当前居住地的时间
# @bp.route('/street/street_typein_resident_info',methods=('GET','POST'))
# @login_required
# def street_typein_resident_info():
#     if request.method == 'POST':
#         pid = request.form['pid']
#         name = request.form['name']
#         phone = request.form['phone']
#         sex = request.form['sex']
#         birth = request.form['birth']
#         street = request.form['street']
#         come_date = request.form['come_date']
#         leave_date = request.form['leave_date']
#         uploaded_file = request.files['file']

#         #输入上传
#         if len(pid)==0 or len(name)==0 or len(sex)==0 or len(phone)==0 or
#             len(birth)==0 or len(street)==0 or len(come_date)==0 or len(leave_date)==0:
#             flash("请输入完整的居民信息")
#         else:
#             single_insert_Residence_info(pid,name,phone,sex,birth,street,come_date,leave_date):
#             flash("录入成功！")

#         #文件上传
#         flag = 0
#         filename = secure_filename(uploaded_file.filename)
#         if filename != '':
#             file_suf = os.path.splitext(filename)[1]
#             if file_suf != '.csv':
#                 flash("仅支持csv文件上传")
#             else:
#                 with open(uploaded_file,'r',encoding='utf-8') as csvfile:
#                     reader = csv.reader(csvfile)
#                     next(reader)
#                     for row in reader:
#                         single_insert_Residence_info(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
#                     flash("居民信息导入成功！")

#     return render_template('street/street_typein_resident_info.html')    
# #2、记录该街道场所的人员流动信息，即场所码的扫码结果录入
# @bp.route('/street/street_typein_site_code_info',methods=('GET','POST'))
# @login_required
# def street_typein_site_code_info():
#     if request.method == 'POST':
#         site_code = request.form['site_code']
#         resident_id = request.form['resident_id']
#         date_time = request.form['date_time']
#         uploaded_file = request.files['file']

#         #输入上传
#         if len(site_code)==0 or len(resident_id)==0 or len(date_time)==0:
#             flash("请输入完整的场所扫码信息")
#         else:
#             single_insert_Scan_code_info(site_code,resident_id,date_time)
#             flash("录入成功！")

#         #文件上传
#         flag = 0
#         filename = secure_filename(uploaded_file.filename)
#         if filename != '':
#             file_suf = os.path.splitext(filename)[1]
#             if filename != '.csv':
#                 flash("仅支持csv文件上传")
#             else:
#                 with open(uploaded_file,'r',encoding='utf-8') as csvfile:
#                     reader = csv.reader(csvfile)
#                     next(reader)
#                     for row in reader:
#                         single_insert_Scan_code_info(row[0],row[1],row[2])
#                     flash("场所扫码信息导入成功！")
#     return render_template('street/street_typein_site_code_info.html')

# #3、录入该街道的小区/场所的相关信息 
# @bp.route('/street/street_typein_site_info.html',methods=('GET','POST'))
# @login_required
# def street_typein_site_info():
#     if request.method == 'POST':
#         site_name = request.form['site_name']
#         site_code = request.form['site_code']
#         locat_street = request.form['locat_street']
#         principal = request.form['principal']
#         contact_num = request.form['contact_num']
#         uploaded_file = request.files['file']

#         #输入上传
#         if len(site_name)==0 or len(site_code)==0 or len(locat_street)==0 or len(principal)==0 or len(date_time)==0:
#             flash("请输入完整的场所信息")
#         else:
#             single_insert_Location_info(site_name,site_code,locat_street,principal,contact_num)
#             flash("录入成功！")
            
#         #文件上传
#         fla = 0
#         filename = secure_filename(uploaded_file.filename)
#         if filename != '':
#             file_suf = os.path.splitext(filename)[1]
#             if filename != '.csv':
#                 flash("仅支持csv文件上传")
#             else:
#                 with open(uploaded_file,'r',encoding='utf-8') as csvfile:
#                     reader = csv.reader(csvfile)
#                     next(reader)
#                     for row in reader:
#                         single_insert_Location_info(row[0],row[1],row[2],row[3])
#                     flash("场所信息导入成功！")
#     return render_template('street/street_typein_site_info.html')

# #4、通过姓名、身份证号等查找负责街道的居民信息
# @bp.route('/street/street_inquire_resident_info.html',methods=('GET','POST'))
# @login_required
# def street_inquire_resident_info():
#     if request.method == 'POST':
#         name = request.form['name']
#         pid = request.form['pid']

#         #获取管理员姓名
#         # print(session['account'])
#         # account_name = ''
#         # with open('instance/new_account.csv') as account_file:
#         # csv.reader = csv.reader(account_file)
#         # next(account_file)
#         # for row in account_file:
#         #     if row[1] == session['account']:
#         #         account_name = row[0]
#         #         break
#         #获取管理员所在街道
#         account_name = session['account']
#         street = get_account_street(account_name)

#         if len(name)==0 and len(pid)==0:
#             flash("请输入查询信息")
#         elif len(pid)==0:#姓名查询
#             resident_info = get_resident_info_name(name)
#         elif len(name)==0:#身份证号查询
#             resident_info = get_resident_info_identity(pid)
#         else:
#             flash("仅可选择一种查询方式，其他位置请保持空白")
#         answer_len = len(resident_info)
#         if answer_len == 1:
#             if resident_info[5] != street:
#                 flash("该人员不属于您所管辖的街道，无法查询")
#             else:
#                 return render_template('street/street_inquire_resident_info.html',answer_len = answer_len,resident_info = resident_info)
#         else:
#             flash("查询存在异常，请重试")
#     return render_template('/street/street_inquire_resident_info.html')
                    
        

        