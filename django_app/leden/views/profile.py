import datetime
import uuid
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from shiften.models import Shift
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from leden import stats
from constance import config


@login_required()
def index(request):
    return render(request, "leden/profile/main.html")


@login_required()
def index(request):
    return render(request, "leden/profile/main.html")


@login_required()
def userinfo(request):
    return render(request, "leden/profile/profile.html")


@login_required
def userical(request):
    context = {}
    if request.method == "POST":
        request.user.lid.ical_token = uuid.uuid4()
        request.user.lid.save()
    if request.user.lid.ical_token:
        context[
            "url"
        ] = f"{request.scheme}://{get_current_site(request)}{reverse('ical_feed', kwargs={'ical_token': request.user.lid.ical_token})}"
    else:
        context["url"] = ""
    return render(request, "leden/profile/ical.html", context)


@login_required()
def usershifts(request):
    shifts = Shift.objects.filter(shifters__id=request.user.lid.id).order_by("date")
    today = datetime.date.today()
    shift_history = shifts.filter(date__lt=today).reverse()
    upcomming_shifts = shifts.filter(date__gte=today)
    context = {
        "shift_history": shift_history,
        "upcomming_shifts": upcomming_shifts,
    }
    return render(request, "leden/profile/shifts.html", context=context)


@login_required()
def userstats(request):
    context = {
        "shifts_in_xmonths": stats.shifts_in_x_months(
            request.user.lid, config.MONTHS_PER_SHIFT
        ),
        "months_per_shift": config.MONTHS_PER_SHIFT,
        "total_shifts": stats.total_shifts_done(request.user.lid),
        "days_since_last_shift": stats.days_since_last_shift(request.user.lid),
    }
    return render(request, "leden/profile/stats.html", context=context)
