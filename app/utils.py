from datetime import datetime
from app import app,models,db
import  requests
import config

def telegram_log_update(update):
	print("\n ---------")
	print(datetime.now())
	if update.message:
		print("From: %s %s. (id: %s)\nText: %s"%(update.message.from_user.first_name,update.message.from_user.last_name,update.message.from_user.id,update.message.text))
	elif update.callback_query:
		print("From: %s %s. (id: %s)\nCallBack Data: %s"%(update.callback_query.from_user.first_name,update.callback_query.from_user.last_name,update.callback_query.from_user.id,update.callback_query.data))
