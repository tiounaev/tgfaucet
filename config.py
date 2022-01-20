import os
app_dir = os.path.abspath(os.path.dirname(__file__))


# YMONEY Settings

YMONEY_SETTINGS = {
    "appname":"TGF",
    "client_id":"65A55FBDA308A6CAE7C7143592807531FC6E948211A882962C0CEF404D2DCFBD",
    "client_secret":"0C315A353D3A97A26A5C032F4F74DA2B6B27C9514E496E4FEE1FDC3AF09B3CE1C11E9A18545F1AC032AFF58170D751472B0246471625B7F3CB3AE9FFCC76D64A"
}


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
LOAD_LANGUAGE_FROM_FILE = os.environ.get('LOAD_LANGUAGE_FROM_FILE',True)

REFERAL_SETTINGS = {
    "bonus_for_referal_after_register":0.5,
    "bonus_for_referal_after_active":0.2,
    "bonus_for_referal_after_active_need_count":10,
    "first_lvl_work_bonus_percent":15,
    "first_lvl_work_bonus_additional":0.75,
    "first_lvl_bonus_percent_for_balans_up":5,
    "second_lvl_work_bonus":5,
    "second_lvl_work_bonus_additional":0.05,
}




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
