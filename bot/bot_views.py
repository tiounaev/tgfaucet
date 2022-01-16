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

    # Register new user
    new_user = models.BotUser(user_id=message.from_user.id,name=str(message.from_user.first_name),username=str(message.from_user.username),language="ru")
    db.session.add(new_user)
    db.session.commit()
    language = language_check(message.from_user.id)
    bot.send_message(message.chat.id,language["register"]["welcome_text"],reply_markup=menu.create_markup(language["register"]["main_menu_keyboard"],row=2))

    # Referal system check
    if len(str(message.text).split(" ")) == 2:
        try:
            referal_id = int(str(message.text).split(" ")[1])
        except:
            referal_id = None
        if referal_id:
            user = models.BotUser.query.filter_by(user_id=referal_id).first()
            if user:
                second_lvl_referal = models.UserReferal.query.filter_by(referal_user_id=user.user_id,second=False).first()
                if second_lvl_referal:
                    second_ref_user = models.BotUser.query.filter_by(user_id=second_lvl_referal.referal_for_user_id).first()
                    if second_ref_user:
                        new_second_lvl_hystory = models.UserBalanseChange(user_id=user.user_id,tag="second_lvl_referal",second_tag="register_bonus",count=config.REFERAL_SETTINGS["bonus_for_referal_after_register"])
                        second_ref_user.balanse = float(second_ref_user.balanse) + config.REFERAL_SETTINGS["bonus_for_referal_after_register"]
                        new_second = models.UserReferal(referal_user_id=message.chat.id,referal_for_user_id=second_lvl_referal.referal_for_user_id,second=True)
                        db.session.add(new_second)
                        db.session.add(new_second_lvl_hystory)
                new_referal = models.UserReferal(referal_user_id=message.chat.id,referal_for_user_id=user.user_id)
                new_first_lvl_hystory = models.UserBalanseChange(user_id=user.user_id,tag="first_lvl_referal",second_tag="register_bonus",count=config.REFERAL_SETTINGS["bonus_for_referal_after_register"])
                db.session.add(new_referal)
                db.session.add(new_first_lvl_hystory)
                user.balanse = float(user.balanse) + config.REFERAL_SETTINGS["bonus_for_referal_after_register"]
                db.session.commit()


#####################--Главное меню --################################################



# ----Заработать----
@bot.message_handler(func=lambda message: message.text and  message.text == language_check(message.from_user.id)['register']["main_menu_keyboard"][0])
def main_menu_for_user_update(message):
    language = language_check(message.chat.id)
    bot.send_message(message.chat.id,"В данный момент для вас нет доступных заданий... Попробуйте позже")

# ----Прокачать----
@bot.message_handler(func=lambda message: message.text and  message.text == language_check(message.from_user.id)['register']["main_menu_keyboard"][1])
def main_menu_for_orderer_update(message):
    language = language_check(message.chat.id)
    bot.send_message(message.chat.id,"Ошибка... Функция отключена администратором (SKIP_NOT_DEV_USER_ID=True)")

# ----Личный кабинет----
@bot.message_handler(func=lambda message: message.text and  message.text == language_check(message.from_user.id)['register']["main_menu_keyboard"][3])
def main_menu_cab_update(message):
    language = language_check(message.chat.id)
    my_user = models.BotUser.query.filter_by(user_id=message.chat.id).first()
    bot.send_message(message.chat.id,language["main_menu"]["cab"]["text"].format(my_user.balanse,my_user.adb_balanse),reply_markup=menu.get_cab_markup(language))


# ----Реферальная система----
@bot.message_handler(func=lambda message: message.text and  message.text == language_check(message.from_user.id)['register']["main_menu_keyboard"][2])
def main_menu_referal_update(message):
    language = language_check(message.chat.id)
    my_link = "https://t.me/{}?start={}".format(bot.get_me().username,message.chat.id)
    total_start_bonus = config.REFERAL_SETTINGS["bonus_for_referal_after_register"] + config.REFERAL_SETTINGS["bonus_for_referal_after_active"]
    my_ref_master_name = language["main_menu"]["referal_system"]["none_referal"]
    my_ref_master = models.UserReferal.query.filter_by(referal_user_id=message.chat.id,second=False).first()
    if my_ref_master:
        if my_ref_master.username:
            my_ref_master_name = my_ref_master.username
        else:
            my_ref_master_name = my_ref_master.name

    first_lvl_ref_count = models.UserReferal.query.filter_by(referal_for_user_id=message.chat.id,second=False).count()
    claim_for_first_lvl_ref = 0
    for ref_plus in  models.UserBalanseChange.query.filter_by(tag="first_lvl_referal",plus=True).all():
        claim_for_first_lvl_ref += ref_plus.count


    second_lvl_ref_count = models.UserReferal.query.filter_by(referal_for_user_id=message.chat.id,second=True).count()
    claim_for_second_lvl_ref = 0
    for ref_plus in  models.UserBalanseChange.query.filter_by(tag="second_lvl_referal",plus=True).all():
        claim_for_second_lvl_ref += ref_plus.count
    format_args = dict(
            total_reg_bonus=total_start_bonus,after_reg_bonus=config.REFERAL_SETTINGS["bonus_for_referal_after_register"],\
            bonus_after_active=config.REFERAL_SETTINGS["bonus_for_referal_after_active"],bonus_after_active_after_count=config.REFERAL_SETTINGS["bonus_for_referal_after_active_need_count"],my_ref=my_ref_master_name,\
            first_lvl_ref_count=first_lvl_ref_count,first_lvl_ref_claim=claim_for_first_lvl_ref,second_lvl_referal_count=second_lvl_ref_count,second_lvl_referal_claim=claim_for_second_lvl_ref,\
            first_lvl_work_bonus=config.REFERAL_SETTINGS["first_lvl_work_bonus_percent"],first_lvl_work_bonus_additional=config.REFERAL_SETTINGS["first_lvl_work_bonus_additional"],\
            first_lvl_balans_up_bonus=config.REFERAL_SETTINGS["first_lvl_bonus_percent_for_balans_up"],second_lvl_work_bonus=config.REFERAL_SETTINGS["second_lvl_work_bonus"],second_lvl_work_bonus_additional=config.REFERAL_SETTINGS["second_lvl_work_bonus_additional"],my_link=my_link)
    bot.send_message(message.chat.id,language["main_menu"]["referal_system"]["post"].format(**format_args) )




# ----Инфо----
@bot.message_handler(func=lambda message: message.text and  message.text == language_check(message.from_user.id)['register']["main_menu_keyboard"][4])
def main_menu_info_update(message):
    language = language_check(message.chat.id)
    bot.send_message(message.chat.id,language["main_menu"]["info"])



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
