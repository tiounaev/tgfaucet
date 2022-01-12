import config
import telebot
import time
from .app import bot,fsm,tbf
from .app import language_sdk
from tb_forms import validators as tbf_validators
from . import keyboards as menu
from . import forms
from .bot_utils import language_check,isCallBackPrefix,get_language_with_code
from app import models,db,app,another_tg_login,app
from datetime import datetime


# Инциализация глобальных насроек TBForm
tbf.GLOBAL_CANCEL_BUTTON_TEXT = lambda user_id: language_check(user_id)["cancel_button"]
tbf.GLOBAL_STOP_FREEZE_TEXT = lambda user_id: language_check(user_id)["freeze_form_alert"]
tbf.GLOBAL_INVALID_INPUT_TEXT = lambda user_id: language_check(user_id)["invalid_input"]


#####################--Регистрация--################################################


# ----Первое сообщение боту----
@bot.message_handler(commands=['start'])
def start_update(message):
    if models.BotUser.query.filter_by(user_id=message.from_user.id).first(): # Пользователь уже зарегистрирован
        language = language_check(message.from_user.id)
        bot.send_message(message.chat.id,language["welcome_again"],reply_markup=menu.create_markup(language["register"]["main_menu_keyboard"],row=2))
        return
    new_user = models.BotUser(user_id=message.from_user.id,name=str(message.from_user.first_name),username=str(message.from_user.username),language="ru")
    db.session.add(new_user)
    db.session.commit()
    bot.send_message(call.message.chat.id,language["welcome_text"],reply_markup=menu.create_markup(language["register"]["main_menu_keyboard"],row=2))




#####################--Технические--################################################

# ---- Разрешить вход в веб-панель ----
@bot.callback_query_handler(func=lambda call: True and call.data == config.admin_another_login_accept_callback)
def another_accept_admin_update(call):
    user_id = int(call.from_user.id)
    bot.delete_message(call.message.chat.id,call.message.message_id)
    another_tg_login.accept_login_session(user_id)


# ----Закрыть форму----
@tbf.global_cancel()
def global_cancel_form(call,form_data):
    language = language_check(call.message.chat.id)
    bot.send_message(call.message.chat.id,language["canceled"])



# ----Отменить ввод----
@bot.callback_query_handler(func=lambda call: call.data == "cancel_hundler")
def cancel_handler_update(call):
    language = language_check(call.from_user.id)
    fsm.reset_state(call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=language["canceled"])
