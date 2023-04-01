import json
import os
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from shiften.models import Shift, Shiftlijst
import datetime
from django.utils.translation import gettext as _
from shiften.models import Onbeschikbaar, OnbeschikbaarHerhalend
from django.db.models import Q
from itertools import chain
import calendar

def create_month_shiftlist(template, date):
    schedule = template.template["schedule"] 
    
    # date = datetime.date.fromisoformat(date)
    date = datetime.date(date.year, date.month, 1)
    list = Shiftlijst.objects.create(type='month', date = date)
    date += datetime.timedelta(days = (schedule[0]["day"] - date.isoweekday() + 7) % 7) 
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

def get_aviable_shifters(shiftlist):
    dict = {}
    # if request.user.has_perm("shiften.view_onbeschikbaar"):
    dict["available"] = []

    list_first_day = shiftlist.date.replace(day=1)
    next_month = shiftlist.date.replace(day=28) + datetime.timedelta(days=4)
    list_last_day = next_month - datetime.timedelta(days=next_month.day)

    avail = Onbeschikbaar.objects.filter(Q(start__lte=list_last_day) & Q(end__gte=list_first_day))
    avail_rep = OnbeschikbaarHerhalend.objects.filter(Q(start_period__lte=list_last_day) & Q(end_period__gte=list_first_day))
    avail_joined = list(chain(avail, avail_rep))
    for a in avail_joined:
        if type(a) == Onbeschikbaar:
            dict["available"].append({
                "date": f"{a.start} - {a.end}",
                "start": a.start,
                "end": a.end,
                "info": a.info,
                "lid": str(a.lid),       
                "user_id": a.lid.user.id,
                "type": "normal"
            })
        if type(a) == OnbeschikbaarHerhalend:
            subdivided = []
            # if a.weekday == list_first_day.isoweekday():
            #     loopday
            loopday = (a.weekday - list_first_day.isoweekday() + 7)%7
            if (list_first_day < a.start_period):
                while (loopday < a.start_period.day):
                    loopday += 7 
            # if a.start_period.isoweekday() < a.weekday:
                # start_period_move += datetime.timedelta(a.weekday - a.start_period.isoweekday() - 1)
            # loopday = start_period_move.day
            while (loopday < list_last_day.day) and ( (list_first_day + datetime.timedelta(days=loopday)) <= a.end_period):
                subdivided.append({
                    "date": list_first_day + datetime.timedelta(days=loopday),
                    "start_time": a.start.isoformat(timespec = "minutes"),
                    "end_time": a.end.isoformat(timespec = "minutes"),
                    "info": a.info,
                    "lid": str(a.lid),
                })
                loopday += 7
            dict["available"].append({
                "date": f"{a.start_period} - {a.end_period}\n{_(calendar.day_name[a.weekday - 1])}\n{a.start} - {a.end}",
                "info": a.info,
                "lid": str(a.lid),
                "user_id": a.lid.user.id,
                "subs": subdivided,
                "type": "rep"
            })
    dict["available"].sort(key=lambda x: x["date"])
    return dict["available"]