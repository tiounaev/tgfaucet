from dotenv import load_dotenv
load_dotenv()
from flask_script import Manager, Shell
from app import app, db,models
from flask_migrate import Migrate, MigrateCommand
from bot.bot_views import bot
import os
import config
import time


# Возвращает переменные, доступные внутри оболочких
def make_shell_context():
    return dict(app=app, db=db)


# Инициализируем приложение в flask_script
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def polling_mode():
    """ Команда запуска бота в режиме polling """
    print("START BOT: {}".format(bot.get_me().username))
    bot.remove_webhook()
    bot.polling(True)


@manager.command
def set_webhook():
    """ Устанвить вебхук для бота"""
    bot.remove_webhook()
    test = bot.set_webhook(config.BASE_DOMAIN + app.config["TOKEN"])
    print("{} SET FOR BOT: {} (DOMAIN: {})".format(test,bot.get_me().username,config.BASE_DOMAIN))
    exit()




if __name__ == '__main__':
    manager.run()
