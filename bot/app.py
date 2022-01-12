from telebot import TeleBot
from tb_forms import TelebotForms,ffsm
from app import redis_client,app,db,models
from . language import Language
import config


# Создаём обьект бота
bot = TeleBot(app.config["TOKEN"])
language_sdk = Language(redis_client)

# Создаем обьект ФСМ и библиотеки TBForms
fsm = ffsm.RedisFSM(redis_client)
tbf = TelebotForms(bot,fsm=fsm)
