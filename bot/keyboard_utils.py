from keyboa import keyboa_maker,keyboa_combiner
from utils import split_list
import telebot


def create_inline_markup(key_dict: dict,row=None):
	""" Создать инлайн клавиатуру из словаря """
	key_list = []
	for key in key_dict:
		data = key_dict[key]
		key_list.append({key:data})
	return keyboa_maker(items=key_list, items_in_row=row)


def create_inline_markup_from_list(key_list: list,front_marker=None):
	""" Создать инлайн клавиатуру из списка """
	return keyboa_maker(items=available_weight, copy_text_to_callback=True,front_marker=front_marker)



def create_markup(key:list, row=0):
    """Создать репли клавиатуру из списка"""
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    if row == 0 or row == 1:
        if isinstance(key, str):
            user_markup.add(key)
        else:
            for i in key:
                user_markup.add(i)
    else:
        key_list = key
        for i in split_list(key_list, row):
            user_markup.add(*[telebot.types.KeyboardButton(name)
                              for name in i])
    return user_markup



def reply_markup_combiner(*keyboards):
    """Комбинирование репли клавиатур"""
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    answer = []
    for i in keyboards:
        for x in i.keyboard:
            answer.append(x)
    for i in answer:
        if list(i) == i:
            user_markup.add(
                *[telebot.types.KeyboardButton(name['text']) for name in i])
        else:
            user_markup.add(i['text'])
    return user_markup
