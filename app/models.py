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
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return auto_repr(self)



class BotAdmin(db.Model):
    """ Админ в боте
    - admin - администратор
    """
    __tablename__ = 'bot_admins'
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'),primary_key=True)
    role = db.Column(db.String(50),default="admin")

    def __repr__(self):
        return auto_repr(self)



class BotPriceParam(db.Model):
    """ Админ в боте """
    __tablename__ = 'bot_price_param'
    id = db.Column(db.Integer(), primary_key=True)
    sub_price = db.Column(db.Float())
    sub_price_percent = db.Column(db.Float())
    join_price = db.Column(db.Float())
    join_price_percent = db.Column(db.Float())
    view_price = db.Column(db.Float())
    view_price_percent = db.Column(db.Float())
    mult_view_price = db.Column(db.Float())
    multi_view_price_percent = db.Column(db.Float())
    first_lvl_referal_balanse_percent = db.Column(db.Float())
    first_lvl_referal_work_percent = db.Column(db.Float())
    second_lvl_referal_balanse_percent = db.Column(db.Float())
    second_lvl_referal_work_percent = db.Column(db.Float())


    def __repr__(self):
        return auto_repr(self)



class SubscribeOrderType(db.Model):
    """ Заказ на подписку\вступление """
    __tablename__ = 'bot_subscribe_order_types'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    count = db.Column(db.Integer())
    one_sub_price = db.Column(db.Float())
    chat_id = db.Column(db.BigInteger())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean(),default=True)


class SubscribeOrderWorker(db.Model):
    """ Исполнение заказа на подписку\вступление """
    __tablename__ = 'bot_subscribe_order_worker'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    order_id = db.Column(db.Integer(), db.ForeignKey(f"{SubscribeOrderType.__tablename__}.id",ondelete='CASCADE'))
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)


class ViewOnePostOrderType(db.Model):
    """ Заказ на просмотр одного поста """
    __tablename__ = "bot_view_one_post_order_types"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    count = db.Column(db.Integer())
    one_view_price = db.Column(db.Float())
    chat_id = db.Column(db.BigInteger())
    msg_id = db.Column(db.Integer())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean(),default=True)


class ViewOnePostOrderWorker(db.Model):
    """ Исполнение заказа на просмотр одного поста """
    __tablename__ = 'bot_view_one_post_order_worker'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    order_id = db.Column(db.Integer(), db.ForeignKey(f"{ViewOnePostOrderType.__tablename__}.id",ondelete='CASCADE'))
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)


class ViewMultiPostOrderType(db.Model):
    """ Заказ на просмотр кол-ва постов """
    __tablename__ = "bot_view_multi_post_order_types"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    count = db.Column(db.Integer())
    one_view_price = db.Column(db.Float())
    chat_id = db.Column(db.BigInteger())
    last_msg_id = db.Column(db.Integer())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)
    active = db.Column(db.Boolean(),default=True)

class ViewMultiPostOrderWorker(db.Model):
    """ Исполнение заказа на просмотр кол-ва постов """
    __tablename__ = 'bot_view_multi_post_order_worker'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    order_id = db.Column(db.Integer(), db.ForeignKey(f"{ViewMultiPostOrderType.__tablename__}.id",ondelete='CASCADE'))
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)






class UserReferal(db.Model):
    """ Реферальная связь """
    __tablename__ = 'bot_referals'
    id = db.Column(db.Integer(), primary_key=True)
    referal_user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    referal_for_user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    second = db.Column(db.Boolean(),default=False)



class UserBalanseChange(db.Model):
    """ История изменения баланса

        Main tag:
    > first_lvl_referal - начисления от реферальной системы первого уровня
    > second_lvl_referal - начисления от реферальной системы второго уровня

        Additional tag
    > register_bonus - бонус после регистрации

    """
    __tablename__ = 'user_balanse_change_hystory'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(f"{BotUser.__tablename__}.user_id",ondelete='CASCADE'))
    tag = db.Column(db.String(50))
    second_tag = db.Column(db.String(50))
    plus = db.Column(db.Boolean(),default=True)
    count = db.Column(db.Float())
