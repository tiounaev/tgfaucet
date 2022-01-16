import telebot
from keyboa import keyboa_maker,keyboa_combiner
from .keyboard_utils import create_inline_markup,create_inline_markup_from_list,create_markup,reply_markup_combiner
from .bot_utils import get_language_with_code, language_check



def get_cab_markup(language):
    markup = {
        language["main_menu"]["cab"]["balanse_up_but"]:"my_cab_up_balanse",
        language["main_menu"]["cab"]["adv_balanse_up_but"]:"my_cab_up_adv_balanse",
        language["main_menu"]["cab"]["convert_balanse_up_but"]:"my_cab_convert_balanse"

    }
    return create_inline_markup(markup,row=2)
