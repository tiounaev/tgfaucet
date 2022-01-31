from flask_admin.contrib.sqla import ModelView
from app import app,db,models,admin,redis_client,data_models
from flask_admin import  BaseView,  expose,AdminIndexView
from flask import render_template, url_for,request, redirect,flash
from flask_login import login_required, login_user,current_user, logout_user
from markupsafe import Markup
from datetime import datetime
from pydantic import ValidationError
import json



class UsersPage(ModelView):
    column_list = ('user_id','name','username','balanse')
    column_labels = dict(name="Имя",balanse="Баланс")
    column_descriptions = dict(user_id="ID пользователя в телеграмм",name="Имя пользователя в Telegram")
    form_columns = ('name', 'balanse')
    column_searchable_list = ('user_id','name', 'username')
    can_create = False
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated


class AdminPage(ModelView):
    column_list = ('user_id',)
    column_descriptions = dict(user_id="ID пользователя в телеграмм")
    form_columns = ('user_id',)

    def is_accessible(self):
        return current_user.is_authenticated

class ParamPage(BaseView):

    @expose("/")
    def index(self):
        if models.BotPriceParam.query.count() == 0:
            new_set = models.BotPriceParam(sub_price=2.0,sub_price_percent=30,join_price=2.0,join_price_percent=30,view_price=0.5,view_price_percent=30,mult_view_price=0.2,multi_view_price_percent=30,first_lvl_referal_balanse_percent=5,first_lvl_referal_work_percent=5,second_lvl_referal_balanse_percent=2,second_lvl_referal_work_percent=2)
            db.session.add(new_set)
            db.session.commit()
        current_settings = models.BotPriceParam.query.first()
        return self.render("admin/param.html",current_settings=current_settings)

    @expose('/save_price_param', methods=('POST',))
    def save_price_param(self):
        args = dict(request.form)
        valid = True
        try:
            new_params = data_models.ParamSettings(**args)
        except ValidationError:
            valid = False
        if valid:
            db.session.query(models.BotPriceParam).delete()
            db.session.commit()
            new_set = models.BotPriceParam(sub_price=new_params.sub_price,sub_price_percent=new_params.sub_price_percent,\
                join_price=new_params.join_price,join_price_percent=new_params.join_price_percent,\
                view_price=new_params.view_price,view_price_percent=new_params.view_price_percent,\
                mult_view_price=new_params.mult_view_price,multi_view_price_percent=new_params.multi_view_price_percent,\
                first_lvl_referal_balanse_percent=new_params.first_lvl_referal_balanse_up_bonus,first_lvl_referal_work_percent=new_params.first_lvl_referal_work_bonus,\
                second_lvl_referal_balanse_percent=new_params.second_lvl_referal_balanse_up_bonus,second_lvl_referal_work_percent=new_params.second_lvl_referal_work_bonus)
            db.session.add(new_set)
            db.session.commit()
            flash("Успешно сохранено.")
        else:
            flash("Ошибка...","error")
        return redirect(url_for("price_param.index"))


    def is_accessible(self):
        return current_user.is_authenticated



class ReferalsPage(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_list = ('referal_user_id','referal_for_user_id','second',)
    column_labels = dict(referal_user_id="ID пользователя",referal_for_user_id="ID Реферала",second="Второй уровень?")

class MoneyHystoryPage(ModelView):
    can_create = False
    can_delete = False
    can_edit = False
    column_list = ('user_id','tag','second_tag','plus','count',)
    column_labels = dict(user_id="ID пользователя",tag="Тег",second_tag="Дополнительный тег",plus="Начисление:",count="Сумма")



# INIT ADMIN PANEL
admin.add_view(UsersPage(models.BotUser, db.session,"Все пользователи",category="Пользователи"))
admin.add_view(AdminPage(models.BotAdmin, db.session,'Админы',category="Пользователи"))
admin.add_view(ReferalsPage(models.UserReferal, db.session,'Реферальные связи',category="Пользователи"))
admin.add_view(MoneyHystoryPage(models.UserBalanseChange, db.session,'Движения баланса',category="Финансы"))
admin.add_view(ParamPage("Параметры",endpoint="price_param"))
