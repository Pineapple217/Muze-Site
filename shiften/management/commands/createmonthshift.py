from django.core.management.base import BaseCommand
from datetime import date 
from shiften.functions import create_month_shifts

class Command(BaseCommand): 
    def add_arguments(self, parser):
        parser.add_argument('date')

    def handle(self, *args, **options):
        y, m = options['date'].split('-')
        m = int(m.lstrip('0'))
        y = int(y)
        d = date(y, m, 1) 
        create_month_shifts(d) 
        