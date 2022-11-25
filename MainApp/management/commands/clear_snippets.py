from django.core.management.base import BaseCommand
from MainApp.models import Snippet


class Command(BaseCommand):
    help = """
    Загрузка данных из указанного Json.
    Файл должен располагаться в корне проекта.
    Если файл не указать, то будет попытка загрузки из файла country-by-languages.json
    """

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options.get('username')
        if username:
            deleted, _row = Snippet.objects.filter(user__username=username).delete()
            self.stdout.write(self.style.SUCCESS(f'Удалено {deleted} записей'))
