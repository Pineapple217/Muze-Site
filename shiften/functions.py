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
    
   