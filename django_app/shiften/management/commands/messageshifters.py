from django.core.management.base import BaseCommand

from shiften.functions import message_shifters


class Command(BaseCommand):
    def handle(self, **args):
        message_shifters()