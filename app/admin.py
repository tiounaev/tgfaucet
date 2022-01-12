from flask_admin.contrib.sqla import ModelView
from app import app,db,models,admin,redis_client
from flask_admin import  BaseView,  expose,AdminIndexView
from flask import render_template, url_for,request, redirect,flash
from flask_login import login_required, login_user,current_user, logout_user
from markupsafe import Markup
from datetime import datetime
import json



class UsersPage(ModelView):
    column_list = ('user_id','name','username','balanse',"adb_balanse")
    column_labels = dict(name="Имя",balanse="Баланс",adb_balanse="Рекламный баланс")
    column_descriptions = dict(user_id="ID пользователя в телеграмм",name="Имя пользователя в Telegram")
    form_columns = ('name', 'balanse','adb_balanse')
    column_searchable_list = ('user_id','name', 'username')
    can_create = False
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated


# INIT ADMIN PANEL
admin.add_view(UsersPage(models.BotUser, db.session,"Все пользователи",category="Пользователи"))
