import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
# from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  # auth：蓝图名字,url_prefix会添加到所有与该蓝图关联的URL前面

#登录视图 关联URL/login和login函数
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        db = get_db()
        error = None
        # user = db.execute(
        #    'SELECT * FROM user WHERE username = ?', (username,)
        # ).fetchone() 
        from db.py import check 
        check_result = check(account,password)
        if check_result == 'Not Exists':
            error = 'Incorrect account.'
        elif check_result == 'Wrong':
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['account'] = account
            if check_result == 'medical staff':
                return redirect(url_for('medical_staff'))  
            if check_result == 'street manager': 
                return redirect(url_for('street_manager'))
            if check_result == 'CDC staff':
                return redirect(url_for('CDC_staff'))
        flash(error)
    return render_template('auth/login.html')          #返回登录页面