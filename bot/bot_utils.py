from . import bot_exeption
from .app import language_sdk
from app import db,models
from telebot import TeleBot
import  telebot
import requests
import os
import json
import config


def get_language_with_code(lang_code: str):
	""" Получить языковой файл по коду языка """
	return language_sdk.get(lang_code)



class LanguageData:

    def __init__(self,data):
        self.data = data


    def _fix_str(self,data):
        return data.replace(r'\n', '\n')

    def __getitem__(self, item):
        if isinstance(self.data[item],dict):
            return LanguageData(self.data[item])
        elif isinstance(self.data[item],str):
            return self._fix_str(self.data[item])
        return self.data[item]

    def getVal(self,*args):
        if not args:
            return self.data
        need = self.data
        for arg in args:
            need = need[arg]
        if isinstance(need,str):
            return self._fix_str(need)
        return need


def language_check(user_id: int,from_code=None,from_model=models.BotUser):
    """ Пол учить языковые даныные в соотвествии с языком пользователя """
    code = "ru"
    if user_id and not from_code:
        user_data = from_model.query.filter_by(user_id=user_id).first()
        if not user_data:
            raise bot_exeption.LanguageNotFoundError()
        code = str(user_data.language)
    elif from_code:
        code = from_code
    lang_data = get_language_with_code(code)
    lang_data["__lang_code"] = code
    return LanguageData(lang_data)



def isCallBackPrefix(call,name):
    """ Проверка, является ли CallBack обновление нужным евентом """
    if str(call.data.split(" ")[0]) == name:
        return True
    return False
