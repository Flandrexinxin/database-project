#医务人员功能页面
import os
import csv
import functools
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import(medical_check,medical_typein,medical_cover,medical_check_csv)
from project.auth import(
    login_required
)
bp = Blueprint('medical', __name__)


@bp.route('/medical/medicalmain',methods = ('GET','POST'))
@login_required
def medicalmain():
    user_name=session['user_name']
    print("imhere")
    return render_template('medical/medicalmain.html',user_name=user_name)

@bp.route('/medical/medical_single_upload',methods = ('GET','POST'))
@login_required
def medical_single_upload():
    user_name=session['user_name']
    if request.method == 'POST':
        print("helloquick!")
        pID = request.form['id']
        datetime = request.form['datetime']
        result = request.form['result']
        sample_num = request.form['sample_num']
        error = None

        if len(pID)==0 or len(datetime)==0 or len(result)==0 or len(sample_num)==0:
            error = '请输入完整的录入信息'
            flash(error)

        if error is None:
            temp = list(datetime)
            temp[10] = ' '
            datetime = ''.join(temp)

            print(datetime)
            if medical_check(pID,datetime,result,sample_num) == False:#用户输入的信息格式错误
                error = '请重新检查修正信息格式'
                flash(error)
            else:
                if medical_typein(pID,datetime,result,sample_num) == True:#成功录入
                    flash("录入成功!")
                else:
                    #这里可能需要一个弹窗提示用户此条检测已存在，是否需要替换
                    flash("该条检测号已存在，现已覆盖")
                    medical_cover(pID,datetime,result,sample_num)
    return render_template('medical/medical_single_upload.html',user_name=user_name)
    
@bp.route('/medical/medical_csv_upload',methods = ('GET','POST'))
@login_required
def medical_csv_upload():
    #文件上传
    user_name=session['user_name']
    if request.method == 'POST':
        flag = 0
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename == '':
            flash("请提交文件")
        else:
            file_suf = os.path.splitext(filename)[1]
            if file_suf != '.csv':
                flash("仅支持csv文件上传")
            else:
                uploaded_file.save(os.path.join('instance', filename))
                file_path = os.path.join('instance',filename)
                with open(file_path,'r',encoding='gbk') as csvfile:
                    reader = csv.reader(csvfile)
                    print("im come in")
                    index = next(reader)#去除索引
                    if len(index) != 4:
                        flash("上传的文件应当为4列，请检查")
                    else:
                        for row in reader:
                            print(row)
                        # row[1] = '2022-10-20 12:00'
                        # print(row[1])
                            if medical_check_csv(row[0],row[1],row[2],row[3]) == True:
                                print("im right")
                                if medical_typein(row[0],row[1],row[2],row[3]) == True:
                                    flag = 0
                                else:
                                    flag = 1
                                    flash("上传文件中不应有已上传过的检测号，若需覆盖，请单条上传")
                                    break
                            else:
                                flag = 1
                                flash("存在信息格式不正确，导入中断，请检查")
                                break
                        print(flag)
                        if flag == 0:
                            flash("核酸结果导入成功！")
                    
    return render_template('medical/medical_csv_upload.html',user_name=user_name)
