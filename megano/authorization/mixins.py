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
            {'name': 'Личный кабинет', 'url': 'authorization:profile_details'},
            {'name': 'Профиль', 'url': 'authorization:profile'},
            # {'name': 'История заказов', 'url': 'authorization:history_order', 'id': '/history_order/', },
            # {'name': 'История просмотров', 'url': 'authorization:history_view', 'id': '/history_view/', },
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
