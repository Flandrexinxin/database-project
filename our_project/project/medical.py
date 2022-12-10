#医务人员功能页面
import csv
import functools
from werkzeug.utils import secure_filename
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db.py import(
    get_resident_info_name,get_resident_info_identity,get_resident_info_region
)
bp = Blueprint('medical', __name__)


@bp.route('/medical/main',method = ('GET','POST'))
@login_required
def medicalmain():
    return render_template('medical/main.html',posts=posts)

@bp.route('/medical/main',method = ('GET','POST'))
@login_required
def main():
    if request.method = 'POST':
        pID = request.form['id']
        datetime = request.form['datetime']
        result = request.form['result']
        sample_num = request.form['sample_num']
        uploaded_file = request.files['file']
        error = None
        flag = 0

        if result == '阴':
            result = 0
        if result == '阳':
            result = 1
        #输入上传
        if len(pID)==0 or len(datetime)==0 or len(result)==0 or len(sample_num)==0:
            error = '请输入完整的录入信息'
            flash(error)
        if error is None:
            if medical_check(pID,data_time,result,sample_num) = False:#用户输入的信息格式错误
                error = '请重新检查修正信息格式'
                flash(error)
            else:
                if medical_typein(pID,data_time,result,sample_num) = True:#成功录入
                    flash("录入成功!")
                else:
                    #这里可能需要一个弹窗提示用户此条检测已存在，是否需要替换
                    flash("This sample_num has been typed in")
                    medical_cover(pID,data_time,result,sample_num)
        
        #文件上传
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_suf = os.path.splitext(filename)[1]
            if file_suf != '.csv':
                flash("仅支持csv文件上传")
            else:
                with open(uploaded_file,'r',encoding = 'utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)#去除索引
                    for row in reader:
                        row[2] = int(row[2])
                        if medical_check(row[0],row[1],row[2],row[3]) = True:
                            if medical_typein(row[0],row[1],row[2],row[3]) = True:
                                flag = 0
                        else:
                            flag = 1
                            break
                    if flag == 0:
                        flash("所有信息已成功录入！")
                    else:
                        flash("信息格式不正确，录入失败，请检查")
    return render_template('medical/main.html')
    
