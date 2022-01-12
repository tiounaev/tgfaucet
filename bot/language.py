from . import bot_exeption
import requests
import os
import json
import config
import pickle

def get_language_with_code_from_file(lang_code: str):
	""" Получить языковой файл по коду языка """
	path_to_file = str(os.path.abspath(os.path.dirname(__file__))) + f"/default_languages/{lang_code}.json"
	with open(path_to_file,encoding="utf-8") as file:
		data = json.load(file)
	return data


class Language:
    def __init__(self,redis_client):
        self.redis_client = redis_client
        self.prefix = "_language"

    def get_language_with_code_from_file(self,lang_code: str):
    	""" Получить языковой файл по коду языка """
    	path_to_file = str(os.path.abspath(os.path.dirname(__file__))) + f"/default_languages/{lang_code}.json"
    	with open(path_to_file,encoding="utf-8") as file:
    		data = json.load(file)
    	return data

    def set_default_from_file(self,code: str):
        keyname = "{}:{}".format(self.prefix,code)
        data = self.get_language_with_code_from_file(code)
        self.redis_client.set(keyname,pickle.dumps(data))

    def set(self,code: str,data: dict):
        keyname = "{}:{}".format(self.prefix,code)
        self.redis_client.set(keyname,pickle.dumps(data))

    def get(self,code: str):
        keyname = "{}:{}".format(self.prefix,code)
        if config.LOAD_LANGUAGE_FROM_FILE:
            data = get_language_with_code_from_file(code)
            print(data)
        else:
            data = self.redis_client.get(keyname)
        if not data:
            return {}
        elif config.LOAD_LANGUAGE_FROM_FILE:
            return data
        else:
            return pickle.loads(data)
