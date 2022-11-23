#蓝图是一种组织一组相关视图及其他代码的方式
#认证蓝图
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  # auth：蓝图名字,url_prefix会添加到所有与该蓝图关联的URL前面
#注册视图
#@bp.route关联URL/register和register视图函数。当Flask收到一个指向/auth/register的请求时就会调用register视图并把其返回值作为响应。
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST': #如果用户提交了表单，就开始验证用户的输入内容
        username = request.form['username']    #request.form['key']：获取表单数据
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
#登录视图 关联URL/login和login函数
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))         #登陆成功，返回index页面

        flash(error)

    return render_template('auth/login.html')          #返回登录页面
#bp.before_app_request() 注册一个在视图函数之前运行的函数，不论其ULR是什么
#load_logged_in_user检查用户id是否已经储存在session中，并从数据库中获取用户数据，然后储存在g.user中。g.user的持续时间比请求要长。如果没有用户id ，或者id不存在，那么g.user将会是None 。
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
#退出登录视图，关联URL/logout和logout函数
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
#用户登录以后才能创建、编辑和删除博客帖子。在每个视图中可以使用装饰器来完成这个工作,装饰器返回一个新的视图，该视图包含了传递给装饰器的原视图。新的函数检查用户是否已载入。如果已载入，那么就继续正常执行原视图，否则就重定向到登录页面。我们会在博客视图中使用这个装饰器
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
