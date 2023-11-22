"""
Модуль с настройками сайта
"""

SECOND = 60
HOURS = 60 * 60
DAYS = 60 * 60 * 24


class Settings:
    """
    Класс с настройками сайта.
    Обновление названия магазина.
    Обновление время кеширования для Баннера, корзины, детализации продуктов, каталога
    """

    def __init__(self):
        """ Значения по умолчанию """
        self.__site_name = 'Megan'
        self.__cache_banner = SECOND * 10  # 10 min
        self.__cache_cart = SECOND * 10  # 10 min
        self.__cache_product = DAYS  # 1 day
        self.__cache_seller = DAYS  # 1 day
        self.__cache_catalog = DAYS  # 1 day

    @staticmethod
    def time_calculate(cache_time) -> str:
        """
        Расчет времени и вывод значений по минутам, часам и дням
        """
        days = cache_time // DAYS
        hours = (cache_time // SECOND) // SECOND  # hours
        minutes = (cache_time // SECOND) % SECOND  # minutes
        if cache_time // SECOND < SECOND:
            return f"{cache_time // SECOND} мин."
        elif 60 <= cache_time // SECOND < 1440:
            return (f"{hours}ч. "
                    f"{str(minutes) + ' мин.' if minutes != 0 else ''}"
                    )
        elif 1440 <= cache_time // SECOND:
            _hours = (cache_time % DAYS) // HOURS
            _minutes = ((cache_time % DAYS) % HOURS) // SECOND
            return (f"{days}д. "
                    f"{str(_hours) + 'ч.' if _hours != 0 else ''} "
                    f"{str(_minutes) + ' мин.' if _minutes != 0 else ''}"
                    )

    def set_site_name(self, name: str) -> None:
        """
        Устанавливает название магазина
        :param name: str Название магазина
        """
        self.__site_name = name

    def set_cache_banner(self, time_cache: int) -> None:
        """
        Устанавливает время кеширование Баннера
        :param time_cache: int время в минутах
        """
        self.__cache_banner = int(time_cache) * SECOND

    def set_cache_cart(self, time_cache: int) -> None:
        """
        Устанавливает время кеширование Корзины
        :param time_cache: int время в минутах
        """
        self.__cache_cart = int(time_cache) * SECOND

    def set_cache_product_detail(self, time_cache: int) -> None:
        """
        Устанавливает время кеширования детальной информации продукта
        :param time_cache:  int время в минутах
        """
        self.__cache_product = int(time_cache) * SECOND

    def set_cache_seller(self, time_cache: int) -> None:
        """
        Устанавливает время кеширования детальной информации продавца
        :param time_cache:  int время в минутах
        """
        self.__cache_seller = int(time_cache) * SECOND

    def set_cache_catalog(self, time_cache: int) -> None:
        """
        Устанавливает время кеширования каталога
        :param time_cache:  int время в минутах
        """
        self.__cache_catalog = int(time_cache) * SECOND

    def get_site_name(self) -> str:
        """
        Возвращает название магазина
        :return: str
        """
        return self.__site_name

    def get_cache_banner(self) -> str:
        """
        Возвращает время хранения кеша Баннера
        :return: int время в минутах
        """
        return self.time_calculate(self.__cache_banner)

    def get_cache_cart(self) -> str:
        """
        Возвращает время хранения кеша Корзины
        :return: int время в минутах
        """
        return self.time_calculate(self.__cache_cart)

    def get_cache_product_detail(self) -> str:
        """
        Возвращает время хранения кеша детальной информации Продукта
        :return: int время в минутах
        """
        return self.time_calculate(self.__cache_product)

    def get_cache_seller(self) -> str:
        """
        Возвращает время хранения кеша данных о продавце
        :return: int время в минутах
        """
        return self.time_calculate(self.__cache_seller)

    def get_cache_catalog(self):
        """
        Возвращает время хранения кеша данных каталога
        :return: int время в минутах
        """

        return self.__cache_catalog


settings = Settings()
