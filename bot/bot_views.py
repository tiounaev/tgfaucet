import config
import telebot
import time
import traceback
from .app import bot,fsm,tbf,ymoney_client
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
    bot.send_message(message.chat.id,language["adv_menu"]["text"],reply_markup=menu.get_adv_menu_markup(language,message.chat.id))


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



#####################--Создание заказа--################################################

# ----Создать новый заказ----
@bot.callback_query_handler(func=lambda call: isCallBackPrefix(call,"adv_menu_new_order"))
def create_new_order_update(call):
    language = language_check(call.message.chat.id)
    bot.delete_message(call.message.chat.id,call.message.message_id)
    form = forms.CreateNewORderForm(language)
    tbf.send_form(call.message.chat.id,form)


# ----Перейти к созданию нового заказа ----
@tbf.form_event("create_new_order",action=["submit"])
def submit_create_order_form_update(call,form_data):
    language = language_check(call.message.chat.id)
    asnwer_map = {
        language["adv_menu"]["create_new_order_form_select_type_vars"][0]:"subscribe",
        language["adv_menu"]["create_new_order_form_select_type_vars"][1]:"subscribe",
        language["adv_menu"]["create_new_order_form_select_type_vars"][2]:"view_post",
        language["adv_menu"]["create_new_order_form_select_type_vars"][3]:"view_multi_post"
    }
    new_order_type = asnwer_map[form_data.order_type]

    if new_order_type == "subscribe":
        sent_msg = bot.send_message(call.message.chat.id,language["create_order"]["create_subscribe_order"]["get_sub_chat_id_text"])
        bot.reply_to(sent_msg,"new_subscribe_order {}".format(call.message.chat.id))



# ----Кол-во подписок для заказа---
@bot.message_handler(content_types=['text'],func=lambda message: True and fsm.get_state(message.chat.id).state == "new_subscribe_order_get_count")
def new_subscribe_order_get_count(message):
    language = language_check(message.chat.id)
    state_args = fsm.get_state(message.chat.id).args
    try:
        count = int(message.text)
    except:
        markup = {language["cancel_button"]:"cancel_hundler"}
        fsm.set_state(message.chat.id,"new_subscribe_order_get_count",channel_id=state_args.channel_id)
        bot.send_message(message.chat.id,language["create_order"]["create_subscribe_order"]["get_sub_count_text"],reply_markup=menu.create_inline_markup(markup))
        return
    fsm.reset_state(message.chat.id)
    markup = {
        language["create_order"]["pay_button"]:"pay_subscribe_order {} {}".format(state_args.channel_id,count)
    }
    current_settings = models.BotPriceParam.query.first()
    price = (current_settings.sub_price * count)
    if (price / int(price)) != 0:
        price = str(int(price)) + "." + str( (price - int(price) ) )[2:4]
    bot.send_message(message.chat.id,language["create_order"]["pay_text"].format(price),reply_markup=menu.create_inline_markup(markup))


# ---- Получаем ид чата для прокачки ----
@bot.message_handler(func=lambda message: str(str(message.text).split(" ")[0]) == "new_subscribe_order" and str(message.chat.type) != "private")
def get_subscribe_chat_id(message):
    user_chat_id = int(str(message.text).split(" ")[1])
    language = language_check(user_chat_id)
    bot.delete_message(message.chat.id,message.message_id)
    markup = {language["cancel_button"]:"cancel_hundler"}
    fsm.set_state(user_chat_id,"new_subscribe_order_get_count",channel_id=message.chat.id)
    bot.send_message(user_chat_id,language["create_order"]["create_subscribe_order"]["get_sub_count_text"],reply_markup=menu.create_inline_markup(markup))


# ----Оплатить заказ на подписки----
@bot.callback_query_handler(func=lambda call: isCallBackPrefix(call,"pay_subscribe_order"))
def pay_subscribe_order_update(call):
    language = language_check(call.message.chat.id)
    user = models.BotUser.query.filter_by(user_id=call.from_user.id).first()
    current_settings = models.BotPriceParam.query.first()
    count = int(call.data.split(" ")[2])
    c_id = int(call.data.split(" ")[1])
    price = (current_settings.sub_price * count)
    if (user.adb_balanse - price) < 0:
        bot.answer_callback_query(call.id,show_alert=True,text=language["create_order"]["no_money_error"])
        return
    bot.delete_message(call.message.chat.id,call.message.message_id)
    user.adb_balanse = (user.adb_balanse - price)
    new_order = models.SubscribeOrderType(user_id=call.from_user.id,count=count,chat_id=c_id)
    db.session.add(new_order)
    db.session.commit()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=language["create_order"]["created"])



# ---- Получаем ид канала для прокачки ----
@bot.channel_post_handler(content_types=['text'])
def channel_post_updater(message):
    if str(str(message.text).split(" ")[0]) == "new_subscribe_order":
        get_subscribe_chat_id(message)


#####################--Технические--################################################



# ----TEST PAYMENTS----
@bot.message_handler(commands=['test'])
def test_update(message):
    try:
        data = ymoney_client.account_info()
        print(data)
    except:
        print(traceback.format_exc())

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
