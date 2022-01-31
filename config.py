import os
app_dir = os.path.abspath(os.path.dirname(__file__))


# YMONEY Settings

YMONEY_SETTINGS = {
    "appname":"TGF",
    "client_id":"65A55FBDA308A6CAE7C7143592807531FC6E948211A882962C0CEF404D2DCFBD",
    "client_secret":"4100116859288179.A420A37FC6538764BFA7C71F685E621D47A60310D6A86C228C7E7125282A75F7C6756BE12B706138020B61C901E1A26D615C3C7F0EDC95A82F53D253E6DC3E4BCB87B27FCDA20A0ED230CB132753036CC9B6ABCCBCE53C7E9B49CA210141098A474DFED6BC2210A7215FB1A3F1E1A641BF3C51ED9E202D6D3563A57AA059D946"
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
    "first_lvl_work_bonus_percent":5,
    "first_lvl_bonus_percent_for_balans_up":5,
    "second_lvl_work_bonus":5,
    "second_lvl_balanse_up_bonus":5,
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
