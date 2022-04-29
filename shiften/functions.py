from gc import get_objects
import os
from discord_webhook import DiscordWebhook
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from shiften.models import Shift, Shiftlijst
from datetime import date, time, timedelta

def create_month_shifts(date: date):
    list = Shiftlijst.objects.create(type='month',
                                        date = date)

    shift_schedule = [(5, [time(15, 30, 00), time(19, 00, 00),
                    time(22, 30, 00), time( 2, 00, 00)]),
                      (6, [time(19, 00, 00),
                    time(22, 30, 00), time( 2, 00, 00)])]
    make_shifts(date, list, shift_schedule)


def make_shifts(date: date, list: Shiftlijst, shift_schedule):
    date += timedelta(days = (shift_schedule[0][0] - date.isoweekday() + 7) % 7)
    month = date.month
    while date.month == month:
        for i in shift_schedule:
            q = date + timedelta(days = i[0] - shift_schedule[0][0])
            for s in range(len(i[1]) - 1):
                Shift.objects.create(date  = q,
                                    start = i[1][s],
                                    end = i[1][s + 1],
                                    shift_list = list
                                    )
        date += timedelta(days = 7)
    
def message_shifters():
    load_dotenv()
    WEBHOOK_URL=os.getenv('WEBHOOK_URL')

    shifts = Shift.objects.filter(date=date.today())
    if len(shifts) > 0:
        content = f"De shifts voor vandaag zijn:\n"
        for shift in shifts:
            content += f"Van {shift.start.isoformat(timespec = 'minutes')} tot {shift.end.isoformat(timespec = 'minutes')}:"
            for lid in shift.shifters.all():
                content += f" <@{lid.discord_id}>"
            content += "\n" 

        webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
        response = webhook.execute() 
    else:
        print('no shifts today')