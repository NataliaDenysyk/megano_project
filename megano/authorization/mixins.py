# from importlib.resources import _


class MenuMixin:

    @staticmethod
    def __menu__() -> list:
        """
        magic method with a menu list.
        :return: list of dictionaries with an available menu.
        :rtype: list
        """
        menu = [
            {'name': 'Личный кабинет', 'url': 'profile:profile_details', 'id': '1', },
            {'name': 'Профиль', 'url': 'profile:profile', 'id': '2', },
            {'name': 'История заказов', 'url': 'profile:history_orders', 'id': '3', },
            {'name': 'История просмотров', 'url': 'profile:history_view', 'id': '4', },
        ]
        return menu

    def get_menu(self, **kwargs) -> dict:
        """
        The method returns the main menu and today's date.
        :param kwargs: accepts the received dictionary.
        :rtype: dict.
        :return: returns the updated dictionary.
        :rtype: dict.
        """

        context = kwargs
        context.update(
            menu=self.__menu__(),
        )

        return context
