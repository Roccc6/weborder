#初始化flask
from flask import Flask

from flask_mysqldb import MySQL
from config import config


mysql = MySQL()
def create_app():
    app = Flask(__name__)
    #注册蓝图
    from .views import bp
    app.register_blueprint(bp)
    app.config.from_object(config['default'])
     # 初始化 MySQL
    mysql.init_app(app)
    return app