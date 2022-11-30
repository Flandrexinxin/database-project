## 医务人员蓝图
#医务人员功能页面
#列出修改/录入/删除核酸检测结果的功能，点击后跳转至相应页面
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db.py import(
    get_resident_info_name,get_resident_info_identity,get_resident_info_region
)
bp = Blueprint('medical', __name__)

# class form1(FlaskForm):
#     inquire = SubmitField('查询')
#     delete = SubmitField('删除')
#     typein = SubmitField('录入')

@bp.route('/medicalmain',method = ('GET','POST'))
@login_required
def medicalmain():
    return render_template('medical/main.html',posts=posts)

@bp.route('/medical/function',method = ('GET','POST'))
@login_required
def function():
    if request.method = 'POST':
        pID = request.form['id']
        #datetime = #这里暂且搁置一下，看TR的日期时间选择器怎么写的再对应抓取
        result = request.form['result']
        sample_num = request.form['sample_num']
        error = None

        if pID == None or data_time == None or result == None or sample_num == None:
            error = 'Please fill in the complete information.'
            flash(error)
        if error is None:
            if medical_check(pID,data_time,result,sample_num) = False:#用户输入的信息格式错误
                error = 'Incorrect input format.'
                flash(error)
            else:
                if medical_typein(pID,data_time,result,sample_num) = True:#成功录入
                    flash("Type in seccess!")
                else:
                    #这里可能需要一个弹窗提示用户此条检测已存在，是否需要替换
                    flash("This sample_num has been typed in")
                    medical_cover(pID,data_time,result,sample_num)



