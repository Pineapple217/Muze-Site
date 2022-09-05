import datetime
from shiften.models import Shift

def total_shifts_done(lid):
    today = datetime.date.today()
    shifts = Shift.objects.filter(shifters__id = lid.id, date__lt = today)

    return shifts.count()
    
def shifts_in_x_months(lid, x):
    shifts = Shift.objects.filter(shifters__id = lid.id)
    today = datetime.date.today()

    shift_history = shifts.filter(date__lt = today)
    print(shift_history)

    if today.month - x <= 0:
        x_months_back = datetime.date(today.year - 1, today.month - x, today.day)
    else:
        x_months_back = datetime.date(today.year, today.month - x, today.day)

    shifts_in_x = shift_history.filter(date__gt = x_months_back)
    print(shifts_in_x.count())
    return shifts_in_x.count()

def days_since_last_shift(lid):
    shifts = Shift.objects.filter(shifters__id = lid.id)
    today = datetime.date.today()

    resent_shift = shifts.filter(date__lt = today).order_by('date').last()
    if resent_shift:
        delta = today - resent_shift.date
        return delta.days
    else:
        return 'n/a'
