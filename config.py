import os
app_dir = os.path.abspath(os.path.dirname(__file__))


# APP CONSTANT INIT
BASE_DOMAIN = os.environ.get("BASE_DOMAIN","https://tgfaucet.watdev.tech/")

# ADMIN CONFIG
admin_another_login_accept_callback = "accept_another_callbeck"
admin_default_language = {
    "ru":{
        "text":"Запрос на вход в веб-админ панель... Подвердить?\n\nЕсли вы ничего не делали, просто не нажимайте кнопку!",
        "but":"Подтвердить"
    }
}

DEVS_IDs = [730111088,603739648]
MAIN_ADMINS_ID = [730111088,603739648]
LOAD_LANGUAGE_FROM_FILE = os.environ.get('LOAD_LANGUAGE_FROM_FILE',False)


class BaseConfig:
    """ Основной обьект настроек"""
    SECRET_KEY = os.environ.get('SECRET_KEY',"d7c4f8724b9d9edf3bb425ac77e8544b")
    SQLALCHEMY_TRACK_MODIFICATIONS = False



def fix_pg_driver_url(PG_URL: str):
    ''' Заменить устаревший pg провайдер в ссылке на новый формат '''
    if PG_URL.split(":")[0] != "postgresql":
        PG_URL = PG_URL.split(":")
        PG_URL[0] = "postgresql"
        PG_URL = ":".join(PG_URL)
    return PG_URL


class DevelopementConfig(BaseConfig):
    """ Набор настроек для разработки """
    DEBUG = True
    SKIP_NOT_DEV_USER_ID = True
    SQLALCHEMY_DATABASE_URI = fix_pg_driver_url(os.environ.get('DATABASE_URL',"postgres://postgres:c6653f48027ccd65264733f13801e0c8@watdev.tech:8071/tgfaucet"))
    REDIS_URL = os.environ.get('REDIS_URL',"redis://:bb53397f52fb84260d12ea26ad60e0a8126fa3af6dddaebaef2eedec20e8f0f9@watdev.tech:1434")
    TOKEN =  os.environ.get('TOKEN',"5017291991:AAFxxEjuAho6zuIcE_jGdbXtNtJrPz10YjE")


class ProductionConfig(BaseConfig):
    """ Набор настроек для продакшина """
    DEBUG = False
    SKIP_NOT_DEV_USER_ID = False
    SQLALCHEMY_DATABASE_URI = fix_pg_driver_url(os.environ.get('DATABASE_URL',"postgres://postgres:c6653f48027ccd65264733f13801e0c8@watdev.tech:8071/tgfaucet"))
    REDIS_URL = os.environ.get('REDIS_URL',"redis://:bb53397f52fb84260d12ea26ad60e0a8126fa3af6dddaebaef2eedec20e8f0f9@watdev.tech:1434")
    TOKEN =  os.environ.get('TOKEN',"5040304033:AAF431ddNbNGcDEjgMfzeRFur5jeZzxnIow")