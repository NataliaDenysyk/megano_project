from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Класс позволяет запустить команду для загрузки файла из консоли.
    Пример: python manage.py upload_file <file_name>
    """
    help = "Позволяет загрузить файл в бд"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Указывает имя файла")

    def handle(self, *args, **options):
        name_file = options.get('file')
        # TODO: здесь метод который будет считывать файл
        test = True
        if test:
            self.stdout.write(f"Файл {name_file}, успешно загружен!")