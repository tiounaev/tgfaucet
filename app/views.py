from app import app
from flask import render_template, request, redirect, url_for, flash, make_response, session,jsonify
from flask_login import login_required, login_user,current_user, logout_user
from . import models,db,redis_client,admin,login_manager,another_tg_login
from . import utils
from bot.bot_views import bot
from . import tg_login
from .utils import telegram_log_update
from datetime import datetime,timedelta
import config
import telebot
import json


@login_manager.user_loader
def load_user(user_id):
	return models.BotUser.query.filter_by(user_id=int(user_id)).first()


# Вебхук для бота заказчиков
@app.route("/{}".format(app.config["TOKEN"]), methods=['POST'])
def order_bot_webhook_update():
	telegram_request = request.stream.read().decode("utf-8")
	update = telebot.types.Update.de_json(telegram_request)
	telegram_log_update(update)
	if app.config["SKIP_NOT_DEV_USER_ID"]:
		if update.message:
			if update.message.from_user.id not in config.DEVS_IDs:
				print("broken")
				bot.send_message(update.message.chat.id,"Тех.работы")
				return "Ok", 200
			elif update.callback_query:
				if update.callback_query.from_user.id in config.DEVS_IDs:
					print("broken")
					bot.send_message(update.callback_query.from_user.id,"Тех.работы")
					return "Ok", 200
	bot.process_new_updates([update])
	return "Ok", 200


@app.route('/')
def index():
	return render_template('index.html',base_domain=config.BASE_DOMAIN,tg_username=bot.get_me().username)


@app.route('/admin_redirect')
@login_required
def admin_redirect():
	return redirect("/admin")

@app.route('/admin/init_app')
@login_required
def admin_init_app():
	flash("Ok")
	if models.BotPriceParam.query.count() == 0:
		new_set = models.BotPriceParam(sub_price=2.0,sub_price_percent=30,join_price=2.0,join_price_percent=30,view_price=0.5,view_price_percent=30,mult_view_price=0.2,multi_view_price_percent=30,first_lvl_referal_balanse_percent=5,first_lvl_referal_work_percent=5,second_lvl_referal_balanse_percent=2,second_lvl_referal_work_percent=2)
		db.session.add(new_set)
		db.session.commit()
		flash("init set")
	return redirect("/admin")



@app.route('/payments_redirect')
def payments_redirect():
	return redirect("https://t.me/tgfzarobotok")


@app.route("/another_login_status", methods=['POST'])
def another_login_status():
	user_id = int(request.form.get("user_id"))
	try:
		data = another_tg_login.get_login_session(int(user_id))
	except tg_login.SessionNotExistError:
		return jsonify(status=False,broke_status=True)
	if data:
		user = models.BotUser.query.filter_by(user_id=int(user_id)).first()
		if user:
			login_user(user, remember=True)
	print(data)
	return jsonify(status=data,broke_status=False)





@app.route("/admin_another_login/<user_id>", methods=['GET'])
def admin_another_login(user_id):
	user = models.BotUser.query.filter_by(user_id=int(user_id)).first()
	if not user:
		return render_template('forbien.html')
	admin = models.BotAdmin.query.filter_by(role="admin",user_id=int(user_id)).first()
	if not admin:
		if int(user_id) not in config.MAIN_ADMINS_ID:
			return render_template('forbien.html')
	try:
		data = another_tg_login.get_login_session(int(user_id))
	except tg_login.SessionNotExistError:
		return "not session sorry"
	return render_template('login_another.html',name=user.name,user_id=user_id)




@app.route("/admin_login", methods=['GET'])
def admin_login():
	tg_data = {
		"id" : request.args.get('id',None),
		"first_name" : request.args.get('first_name',None),
		"last_name" : request.args.get('last_name', None),
		"username" : request.args.get('username', None),
		"auth_date":  request.args.get('auth_date', None),
		"hash" : request.args.get('hash',None)
	}
	if tg_login.data_check(app.config["TOKEN"],tg_data):
		user = models.BotUser.query.filter_by(user_id=int(tg_data["id"])).first()
		if not user:
			return render_template('forbien.html')
		admin = models.BotAdmin.query.filter_by(role="admin",user_id=int(tg_data["id"])).first()
		if not admin:
			return render_template('forbien.html')
		login_user(user, remember=True)
		return redirect("/admin")
	else:
		user = models.BotUser.query.filter_by(user_id=int(tg_data["id"])).first()
		if not user:
			return render_template('forbien.html')
		admin = models.BotAdmin.query.filter_by(role="admin",user_id=int(tg_data["id"])).first()
		if not admin:
			if int(tg_data["id"]) not in config.MAIN_ADMINS_ID:
				return render_template('forbien.html')
		try:
			another_tg_login.create_login_session(int(tg_data["id"]))
		except tg_login.SessionAlreadyExistError:
			pass
		bot = telebot.TeleBot(app.config["TOKEN"])
		texts = config.admin_default_language[user.language]
		markup = telebot.types.InlineKeyboardMarkup()
		markup.add(telebot.types.InlineKeyboardButton(texts["but"], callback_data=config.admin_another_login_accept_callback))
		bot.send_message(int(tg_data["id"]),texts["text"],reply_markup=markup)
		return redirect(url_for('admin_another_login',user_id=tg_data["id"]))
	return redirect(url_for('index'))
