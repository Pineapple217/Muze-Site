import json
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from shiften.models import Shift, Shiftlijst
import datetime

def create_month_shiftlist(template, date):
    schedule = template.template["schedule"] 
    
    # date = datetime.date.fromisoformat(date)
    date = datetime.date(date.year, date.month, 1)
    list = Shiftlijst.objects.create(type='month', date = date)
    date += datetime.timedelta(days = (schedule[0]["day"] - date.isoweekday() + 7) % 7) 
    print(date)
    month = date.month
    while date.month == month:
        for shift in schedule:
            shift_date = date + datetime.timedelta(days = shift["day"] - schedule[0]["day"])
            Shift.objects.create(date  = shift_date,
                                start = shift["start"],
                                end = shift["end"],
                                shift_list = list,
                                max_shifters = shift["max"]
                                )
        date += datetime.timedelta(days = 7)
    return list
    
def message_shifters():
    load_dotenv()
    WEBHOOK_URL=os.getenv('WEBHOOK_URL')

    shifts = Shift.objects.filter(date=datetime.date.today())
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