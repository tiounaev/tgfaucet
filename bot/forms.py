import validators
from tb_forms import BaseForm,fields
from app import db, models


class CreateNewORderForm(BaseForm):
    """ Регистрация пользователей в боте пользователя """
    def __init__(self,language):
        self.update_name = "create_new_order"
        self.form_title = language["adv_menu"]["create_new_order_form_title"]
        texts_data = language["adv_menu"]
        self.order_type = fields.ChooseField(texts_data["create_new_order_form_select_type_but"],texts_data["create_new_order_form_select_type_text"],answer_list=texts_data["create_new_order_form_select_type_vars"],button_in_row=1)
        self.submit_button_text = texts_data["create_new_order_form_submit"]
        self.freeze_mode = True
        self.close_form_but = True
        self.texts_data = texts_data
