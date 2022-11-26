import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db.py import(
    get_resident_info_name,get_resident_info_identity,get_resident_info_region
)
bp = Blueprint('CDC', __name__)

@bp.route('/CDC/main',method = ('GET', 'POST'))
@login_required
def CDCmain():
    return render_template('CDC/main.html',posts=posts)
# 通过姓名、身份证号等查找居民信息，或者浏览某一区域的情况
@bp.route('/CDC/inquire',method=('GET','POST'))
@login_required 
def inquire():
    if request.method == 'POST':
        name = request.form['name']
        identity = request.form['identity']
        region = request.form['region'] 
        error = None

        if len(name) == 0 and len(identity) == 0 and len(region) == 0:
            error = '请输入所查询信息'
        elif len(identity) == 0 and len(region) == 0:
            resident_info = get_resident_info_name(name)
        elif len(name) == 0 and len(region) == 0:
            resident_info = get_resident_info_identity(identity)
        elif len(name) == 0 and len(identity) == 0:
            resident_info = get_resident_info_region(region)
        else:
            error = '仅可选择一种查询方式,请保持其他输入框空白'
        if error is None:
            length = len(resident_info)
            return render_template('auth/login.html',length=length,resident_info)  
