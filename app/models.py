from app import db, login_manager
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_required,login_user, current_user, logout_user
from sqlalchemy.schema import Sequence

def auto_repr(self):
    """ Автоматическое REPR форматирование для обьектов """
    base_repr = "<{}(".format(self.__class__.__name__)
    for name in self.__dict__:
        if name[0] == "_":
            continue
        value = self.__dict__[name]
        base_repr += "{}='{}',".format(name,value)
    base_repr = base_repr[:-1]
    base_repr += ")>"
    return base_repr


class BotUser(UserMixin,db.Model):
    """ Пользователь бота """
    __tablename__ = 'bot_users'
    user_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    username = db.Column(db.String(50))
    language = db.Column(db.String(50),default="ru")
    balanse = db.Column(db.Float(),default=0.0)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return auto_repr(self)



class BotAdmin(db.Model):
    """ Админ в боте
    - admin - администратор
    """
    __tablename__ = 'bot_admins'
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id"),primary_key=True)
    role = db.Column(db.String(50),default="admin")

    def __repr__(self):
        return auto_repr(self)