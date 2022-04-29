from django.core.management.base import BaseCommand
from leden.functions import export_shiftlist 


class Command(BaseCommand):
    def handle(self, **args):
        export_shiftlist()