import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from project.db import (
    check_account, get_user_tuple, get_user_name, change_password
) 
# from werkzeug.security import check_password_hash, generate_password_hash

#from flaskr.db import get_db

bp = Blueprint('auth', __name__)  # auth：蓝图名字,url_prefix会添加到所有与该蓝图关联的URL前面
#登录视图 关联URL和login函数
@bp.route('/', methods=('GET', 'POST'))
def login():
    print("hello")
    if request.method == 'POST':
        print("hi")
        account = request.form['account']
        password = request.form['password']
        print(account,password)
        error = None 
        check_result = check_account(account,password)
        print(check_result)
        if check_result == 'Not Exists':
            error = 'Account not exists.'
        elif check_result == 'wrong':
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['account'] = account
            session['password'] = password
            user_name = get_user_name(account)
            user_name = user_name[0][0]
            print(user_name)
            session['user_name'] = user_name
            if check_result == 'medical staff':
                return redirect(url_for('medical.medicalmain'))  
            if check_result == 'street manager': 
                return redirect(url_for('street.streetmain'))
            if check_result == 'CDC staff':
                return redirect(url_for('CDC.CDCmain'))
            if check_result == 'super manager':
                return redirect(url_for('DB_administrator.DBmain'))
        flash(error)
    return render_template('auth/login.html')          #返回登录页面

@bp.route('/change_pwd',methods=('GET','POST'))
def change_pwd():
    if request.method == 'POST':
        account = request.form['account']
        old_pwd = request.form['old_pwd']
        new_pwd = request.form['new_pwd']
        new_pwd_repeat = request.form['new_pwd_repeat']
        check_result = check_account(account,old_pwd)
        if check_result == 'Not Exists':
            error = '账号不存在'
            flash(error)
        elif check_result == 'wrong':
            error = '密码输入错误' 
            flash(error)
        elif new_pwd != new_pwd_repeat:
            error = '新密码输入不一致，请检查'
        else:
            if_success = change_password(account,new_pwd)
            if if_success == True:
                flash('修改成功')
            else:
                flash('密码不符合要求，须包含数字和字母')  
    return render_template('auth/change_pwd.html')  
               
@bp.before_app_request
def load_logged_in_user():
    user_account = session.get('account')
    if user_account is None:
        g.user = None
    else:
        g.user = get_user_tuple(user_account)
#用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用装饰器来完成这个工作,装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户是否已载入。如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。我们会在博客视图中使用这个装饰器
def login_required(view):
    @functools.wraps(view)    #在编写装饰器时，在实现前加入@functools.wraps(func)可以保证装饰器不会对被装饰函数造成影响
    def wrapped_view(**kwargs):
        if g.user is None:       #如果用户没有登陆，就返回到登陆界面
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
