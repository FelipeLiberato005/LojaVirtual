from flask import Flask
from flask_mysqldb import MySQL
from config import SECRET_KEY, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_HOST
from flask_bcrypt import Bcrypt
import os

mysql = MySQL() #instancia do banco criada aqui
bcrypt = Bcrypt()
UPLOAD_FOLDER = os.path.join('app', 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.secret_key = 'ef4e607f7f192b5607b45528925e59b3'
    app.config['MYSQL_PORT'] = 3307
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = MYSQL_DB
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB máx
    

    mysql.init_app(app)
    bcrypt.init_app(app)
# aqui vai iniciar o MySQL com o app

    from datetime import datetime
    @app.template_filter('datetimeformat')
    def datetimeformat(value, fmt='%d/%m/%Y'):
        if isinstance(value, (datetime,)):
            return value.strftime(fmt)
        return value

    from app.routes import main

    app.register_blueprint(main)
    return app

