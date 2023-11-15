"""
Модуль с настройками сайта
"""

SECOND = 60


class Settings:
    """
    Класс с настройками сайта.
    Обновление названия магазина.
    Обновление время кеширования для Баннера, корзины, детализации продуктов
    """

    def __init__(self):
        """ Значения по умолчанию """
        self.__site_name = 'Megano'
        self.__cache_banner = 600  # 10 min
        self.__cache_cart = 600  # 10 min
        self.__cache_product = 60 * 60 * 24  # 1 day

    def set_site_name(self, name: str) -> None:
        """
        Устанавливает название магазина
        :param name: str Название магазина
        """
        self.__site_name = name

    def set_cache_banner(self, time_cache: int) -> None:
        """
        Устанавливает время кеширование Баннера
        :param time_cache: int время в секундах
        """
        self.__cache_banner = int(time_cache) * SECOND

    def set_cache_cart(self, time_cache: int) -> None:
        """
        Устанавливает время кеширование Корзины
        :param time_cache: int время в секундах
        """
        self.__cache_cart = int(time_cache) * SECOND

    def set_cache_product_detail(self, time_cache: int) -> None:
        """
        Устанавливает время кеширования детальной информации продукта
        :param time_cache:  int время в секундах
        """
        self.__cache_product = int(time_cache) * SECOND

    def get_site_name(self) -> str:
        """
        Возвращает название магазина
        :return: str
        """
        return self.__site_name

    def get_cache_banner(self) -> int:
        """
        Возвращает время хранения кеша Баннера
        :return: int время в минутах
        """
        return self.__cache_banner // SECOND

    def get_cache_cart(self) -> int:
        """
        Возвращает время хранения кеша Корзины
        :return: int время в минутах
        """
        return self.__cache_cart // SECOND

    def get_cache_product_detail(self) -> int:
        """
        Возвращает время хранения кеша детальной информации Продукта
        :return: int время в минутах
        """
        return self.__cache_product // SECOND


settings = Settings()
