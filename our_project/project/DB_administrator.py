import functools
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file, make_response
)
import csv
from project.db import(
    add_staff, create_password,delete_user
)
from project.auth import(
    login_required
)
import os
bp = Blueprint('DB_administrator', __name__)


@bp.route('/DB_administrator/DBmain',methods = ('GET', 'POST'))
@login_required
def DBmain():
    user_name=session['user_name']
    print("Hey I'm coming!")
    return render_template('DB_administrator/DBmain.html',user_name=user_name)


# 生成medical员工账号
@bp.route('/DB_administrator/DBaddmedical',methods = ('GET', 'POST'))
@login_required
def DBaddmedical():
    user_name = session['user_name']
    error = None
    user_names = []
    num =0
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            error = '未提交文件'
        else:
            file_ext = os.path.splitext(filename)[1]
            if file_ext != '.csv':
                 error = "仅支持csv文件的上传"
            if error is None:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader:            # 将csv文件中的数据保存到data中
                        if len(row)!=1:
                            error = '文件格式有误，请保证每行仅包含一个用户姓名'
                        else:
                            num = num+1
                            user_names.append(row[0])  
                if error is None:
                    new_account = create_password(num)          #生成新的账号密码
                    add_staff(new_account,'medical staff',user_names)     #将新的用户加入数据库的基本表
                    header = ['姓名','账号','密码','用户类别']
                    with open('instance/new_account.csv','w') as new:
                        writer = csv.writer(new)
                        writer.writerow(header)
                        for i in range(num):
                            data = [user_names[i],new_account[i][0],new_account[i][1],'医务人员']
                            writer.writerow(data)
                    return redirect(url_for('DB_administrator.DBdownload',next=request.url))
        flash(error)
    return render_template('DB_administrator/DBaddmedical.html',user_name=user_name)    


# 生成CDC员工账号
@bp.route('/DB_administrator/DBaddCDC',methods = ('GET', 'POST'))
@login_required
def DBaddCDC():
    user_name = session['user_name']
    error = None
    user_names = []
    num =0
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            error = '未提交文件'
        else:
            file_ext = os.path.splitext(filename)[1]
            if file_ext != '.csv':
                 error = "仅支持csv文件的上传"
            if error is None:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader:            # 将csv文件中的数据保存到data中
                        if len(row) !=1:
                            error = '文件格式有误，请保证每行仅包含一个用户姓名'
                        else:
                            num = num+1
                            user_names.append(row[0])           # 选择某一列加入到data数组中
                if error is None:
                    new_account = create_password(num)          #生成新的账号密码
                    add_staff(new_account,'CDC staff',user_names)     #将新的用户加入数据库的基本表
                    header = ['姓名','账号','密码','用户类别']
                    with open('instance/new_account.csv','w') as new:
                        writer = csv.writer(new)
                        writer.writerow(header)
                        for i in range(num):
                            data = [user_names[i],new_account[i][0],new_account[i][1],'疾控中心工作人员']
                            writer.writerow(data)
                    return redirect(url_for('DB_administrator.DBdownload',next=request.url))
        flash(error)
    return render_template('DB_administrator/DBaddCDC.html',user_name=user_name) 


# 生成street员工账号
@bp.route('/DB_administrator/DBaddstreet',methods = ('GET', 'POST'))
@login_required
def DBaddstreet():
    user_name = session['user_name']
    error = None
    user_names = []
    streets = []
    num = 0
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            error = '未提交文件'
        else:
            file_ext = os.path.splitext(filename)[1]
            if file_ext != '.csv':
                 error = "仅支持csv文件的上传"
            if error is None:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader:            # 将csv文件中的数据保存到data中
                        if len(row)!=2:
                            error = '文件格式有误，请保证每行包含且仅包含一组用户姓名和管辖街道'
                        else:
                            num = num+1
                            user_names.append(row[0])           # 选择某一列加入到data数组中
                            streets.append(row[1])
                if error is None:
                    new_account = create_password(num)          #生成新的账号密码
                    add_staff(new_account,'street manager',user_names,streets)     #将新的用户加入数据库的基本表
                    header = ['姓名','账号','密码','用户类别','管理街道']
                    with open('instance/new_account.csv','w') as new:
                        writer = csv.writer(new)
                        writer.writerow(header)
                        for i in range(num):
                            data = [user_names[i],new_account[i][0],new_account[i][1],'街道工作人员',streets[i]]
                            writer.writerow(data)
                    return redirect(url_for('DB_administrator.DBdownload',next=request.url))
        flash(error)
    return render_template('DB_administrator/DBaddstreet.html',user_name=user_name) 


# 生成DB_administrator账号
@bp.route('/DB_administrator/DBaddDB',methods = ('GET', 'POST'))
@login_required
def DBaddDB():
    user_name = session['user_name']
    error = None
    user_names = []
    num =0
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            error = '未提交文件'
        else:
            file_ext = os.path.splitext(filename)[1]
            if file_ext != '.csv':
                 error = "仅支持csv文件的上传"
            if error is None:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader:            # 将csv文件中的数据保存到data中
                        if len(row) != 1:
                            error = '文件格式有误，请保证每行仅包含一个用户姓名'
                        else:
                            num = num+1
                            user_names.append(row[0])           # 选择某一列加入到data数组中
                if error is None:
                    new_account = create_password(num)          #生成新的账号密码
                    add_staff(new_account,'super manager',user_names)     #将新的用户加入数据库的基本表
                    header = ['姓名','账号','密码','用户类别']
                    with open('instance/new_account.csv','w') as new:
                        writer = csv.writer(new)
                        writer.writerow(header)
                        for i in range(num):
                            data = [user_names[i],new_account[i][0],new_account[i][1],'系统管理员']
                            writer.writerow(data)
                    return redirect(url_for('DB_administrator.DBdownload',next=request.url))
        flash(error)
    return render_template('DB_administrator/DBaddDB.html',user_name=user_name) 


# 下载新账号
@bp.route('/DB_administrator/DBdownload',methods = ('GET', 'POST'))
@login_required
def DBdownload():
    user_name = session['user_name']
    # return send_from_directory(r"C:\\Users\\Lenovo\\gitee\\database-project\\our_project\\instance","new_account.csv")
    from flask import send_file 
    download_path = '../instance/new_account.csv' 
    response = make_response(send_file(download_path))
    return response


# 删除账号
@bp.route('/DB_administrator/delete',methods = ('GET', 'POST'))
@login_required
def delete():
    user_name = session['user_name']
    error = None
    user_accounts = []
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            error = '未提交文件'
        else:
            file_ext = os.path.splitext(filename)[1]
            if file_ext != '.csv':
                 error = "仅支持csv文件的上传"
            if error is None:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path) as csvfile:
                    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
                    for row in csv_reader:            # 将csv文件中的数据保存到data
                        if len(row) != 1:
                            error = '文件格式有误，请保证每行仅包含一个账号'
                        else:
                            user_accounts.append(row[0])           # 选择某一列加入到data数组   
                if error is None:
                    delete_user(user_accounts) 
        flash(error)  
    return render_template('DB_administrator/delete.html',user_name=user_name) 

