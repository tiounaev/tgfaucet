import hashlib
import hmac
import base64
import time


def string_generator(data_incoming):
    data = data_incoming.copy()
    del data['hash']
    keys = sorted(data.keys())
    string_arr = []
    for key in keys:
        if data[key] != None:
            string_arr.append(key+'='+data[key])
    string_cat = '\n'.join(string_arr)
    return string_cat

def data_check(BOT_TOKEN, tg_data):
    data_check_string = string_generator(tg_data)
    secret_key = hashlib.sha256(BOT_TOKEN.encode('utf-8')).digest()
    secret_key_bytes = secret_key
    data_check_string_bytes = bytes(data_check_string,'utf-8')
    hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
    if hmac_string == tg_data['hash']:
        return True
    else:
        return False



class SessionAlreadyExistError(Exception):
    """ Ошибка альтернативного входа, сессия уже существует  """
    def __init__(self):
        super().__init__("Сессия уже существует, вы не можете создать новую")

class SessionNotExistError(Exception):
    """ Ошибка альтернативного входа, сессии не существует """
    def __init__(self):
        super().__init__("Сессия не существует")



class AnotherTelegramLogin:
    """ Работа с альтернативным входом через бота """
    lifetime = 60
    def __init__(self,redis_client,redis_prefix = "_tg_login_session"):
        self.redis_client = redis_client
        self.redis_prefix = redis_prefix


    def _gen_key_name(self,*args):
        key_name = str(self.redis_prefix)
        for arg in args:
            key_name += ":{}".format(arg)
        return key_name


    def get_login_session(self,user_id: int):
        """ Получить сессию альтернативного входа """
        keyname = self._gen_key_name("login_session",user_id)
        need_data = self.redis_client.get(keyname)
        if need_data == None:
            raise SessionNotExistError()
        print(need_data)
        if need_data == b"True":
            return True
        return False

    def create_login_session(self,user_id: int):
        """ Создать сессию входа """
        keyname = self._gen_key_name("login_session",user_id)
        try:
            self.get_login_session(user_id)
            raise SessionAlreadyExistError
        except SessionNotExistError:
            self.redis_client.setex(keyname,self.lifetime,value="False")
        return True


    def accept_login_session(self,user_id: int):
        """ Принять сессию входа"""
        try:
            self.get_login_session(user_id)
        except SessionNotExistError:
            raise SessionNotExistError
        keyname = self._gen_key_name("login_session",user_id)
        self.redis_client.setex(keyname,self.lifetime,value="True")
        return True
