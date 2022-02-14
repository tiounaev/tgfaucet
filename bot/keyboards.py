import telebot
from keyboa import keyboa_maker,keyboa_combiner
from .keyboard_utils import create_inline_markup,create_inline_markup_from_list,create_markup,reply_markup_combiner
from .bot_utils import get_language_with_code, language_check
from app import models,db,app


def get_cab_markup(language):
    """ Личный кабинет """
    markup = {
        language["main_menu"]["cab"]["balanse_up_but"]:"my_cab_up_balanse",

    }
    return create_inline_markup(markup,row=2)


def get_adv_menu_markup(language,user_id):
    """ Меню рекламодателя """
    subscribe_active_order_count = models.SubscribeOrderType.query.filter_by(user_id=user_id,active=True).count()
    view_one_post_active_order_count = models.ViewOnePostOrderType.query.filter_by(user_id=user_id,active=True).count()
    view_multi_post_active_order_count = models.ViewMultiPostOrderType.query.filter_by(user_id=user_id,active=True).count()
    individual_order_active_count = 0
    count = (subscribe_active_order_count + view_multi_post_active_order_count + view_one_post_active_order_count + individual_order_active_count)
    markup = {
        language["adv_menu"]["active_order_but"].format(count):"adv_menu_to_active",
        language["adv_menu"]["create_new_order_but"]:"adv_menu_new_order"
    }
    return create_inline_markup(markup,row=1)


def get_active_order_menu(language,all_orders):
    """ Список активных заказов """
    markup = {}
    for order in all_orders:
        if isinstance(order,models.SubscribeOrderType):
            order_type = "subscribe"
            order_name = language["active_order"]["subscribe_type"]
        elif isinstance(order,models.ViewOnePostOrderType):
            order_type = "view_one_post"
            order_name = language["active_order"]["view_post_type"]
        elif isinstance(order,models.ViewMultiPostOrderType):
            order_type = "view_multi_post"
            order_name = language["active_order"]["view_multi_post_type"]
        markup[language["active_order"]["but_text_format"].format(order_name,order.id)] = "select_active_order {} {}".format(order_type,order.id)
    markup[language["back"]] = "back_to_orders_menu"
    return create_inline_markup(markup,row=1)
