from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from services.services import ImportJSONService

import os
import re


class Command(BaseCommand):
    """
    Класс позволяет запустить команду для загрузки файла из консоли.
    Пример: python manage.py upload_file <file_name>
    """
    help = "Позволяет загрузить файл в бд"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Указывает имя файла")
        parser.add_argument('-e', '--email', action='store_true', help="Подключает отправку сообщений на почту")

    def handle(self, *args, **options):
        path_work_dir = os.path.abspath(os.path.join(''))
        file_name = options.get('file')
        file = self.search_file(path_work_dir, file_name)
        name_file = self.cleaned_name(file)
        import_file = ImportJSONService()

        with open(file, 'r', encoding='utf-8') as file_json:
            try:
                messages = import_file.import_json(file_json, name_file)
                if options['email']:
                    send_mail(f'Загрузка файла "{file_name}"',
                              f'Отчет по загрузке файла "{file_name}":\n'
                              f'{[mes for mes in messages]}',
                              'megano@qwe.com', ['root@qwe.ru'], fail_silently=False)
                self.stdout.write(f'Файл "{file_name}", успешно загружен!')
            except Exception as err:
                self.stdout.write(f'Файл "{file_name}": Загружен с ошибкой.\nОШИБКА: {err}')

    @staticmethod
    def search_file(path_work_dir, file_name):
        """
        Поиск файла по названию или в переданной директории
        """
        dir_name = os.path.isdir(file_name)
        if dir_name:
            path_work_dir = os.path.join(path_work_dir, file_name)

        for root, dirs, files in os.walk(path_work_dir):
            for file in files:
                __file = re.findall(r'.json', file)
                if (__file and file_name == file) or (__file and dir_name):
                    return os.path.join(root, file)

    @staticmethod
    def cleaned_name(file):
        """
        Очистка файля от расширения
        """
        name = re.findall(r'[^\\/]+', file)[-1].split('.')[0]
        return name
