
class LanguageNotFoundError(Exception):
    """ Попытка получить язык у несуществующего пользователя"""
    def __init__(self):
        super().__init__("Language of this user not defind.")
