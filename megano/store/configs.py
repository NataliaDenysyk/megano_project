"""
Модуль с настройками сайта
"""

class Settings:

    def __init__(self):
        self.__site_name = ''

    def set_site_name(self, name):
        self.__site_name = name

    def get_site_name(self):
        return self.__site_name


settings = Settings()
