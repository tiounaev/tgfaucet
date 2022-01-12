from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_admin import Admin
from .admin_home import HomeView
from flask_babelex import Babel
from .tg_login import AnotherTelegramLogin
import os
import config
import logging

# Создаем экземпляр приложения
app = Flask(__name__)
app.logger.setLevel(logging.ERROR)
app.config.from_object(os.environ.get('START_AS','config.ProductionConfig'))

# Инициализация базы данных
db = SQLAlchemy(app)
redis_client = FlaskRedis(app)

# Инициализация Flask расширений
login_manager = LoginManager(app)
login_manager.login_view = '/'

babel = Babel(app)
@babel.localeselector
def get_locale():
        return 'ru'

admin = Admin(app,template_mode='bootstrap4',index_view=HomeView())
another_tg_login = AnotherTelegramLogin(redis_client)


# Подгружаем все маршртуы
from . import views
from .admin import admin
