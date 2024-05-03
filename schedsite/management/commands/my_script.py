from django.core.management.base import BaseCommand
from main import *


def execute_main():
    main()


class MyCommand(BaseCommand):
    help = 'Description of your command'

    def handle(self, *args, **options):
        # Code to execute your main.py script logic here
        # You can access settings using self.settings
        # Access models using self.stdout.write(...) for output

        pass
