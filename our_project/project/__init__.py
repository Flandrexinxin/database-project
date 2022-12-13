#__init__.py的作用:包含应用工厂、告诉Python，flaskr文件夹应视作一个包
import os

from flask import Flask
from project.auth import login
#可以在一个函数内部创建 Flask 实例来代替创建全局实例。
#这个函数被称为应用工厂。
#所有应用相关的配置、注册和其他设置都会在函数内部完成，然后返回这个应用。

#create_app是一个应用工厂函数
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)  #创建flask实例
    app.config.from_mapping(
        SECRET_KEY='dev',           #SECRET_KEY可用于写哈希给密码加密
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  #路径拼接 
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config['UPLOAD_EXTENSIONS'] = ['.csv']
    app.config['UPLOAD_PATH'] = 'instance'

    from . import auth
    app.register_blueprint(auth.bp)
    from . import CDC
    app.register_blueprint(CDC.bp)
    from . import DB_administrator
    app.register_blueprint(DB_administrator.bp)
    from . import medical
    app.register_blueprint(medical.bp)
    # from . import street
    # app.register_blueprint(street.bp)
    app.add_url_rule('/',endpoint='login')
    return app
# view_func=login