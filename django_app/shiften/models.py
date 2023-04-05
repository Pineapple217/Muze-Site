import datetime
from django.db import models

from leden.models import Lid
from django.utils.translation import gettext as _
from django.utils import formats
from simple_history.models import HistoricalRecords

from django.core.exceptions import ValidationError

# from datetime import datetime, time, timedelta, date
from django.urls import reverse
from constance import config


class Shiftlijst(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField()
    TYPES = [("month", _("month")), ("event", _("event"))]
    type = models.CharField(max_length=100, choices=TYPES)
    is_active = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        if self.type == "month" and type(self.date) == datetime.date:
            return _(formats.date_format(self.date, format="F Y"))
        else:
            if self.name:
                return self.name
        return "ERROR __str__"

    def clean(self):
        if self.type != "month":
            if not self.name:
                raise ValidationError(
                    {"name": "Name can only be empty if it is of type month"}
                )
        if self.type == "month":
            self.date = datetime.date(self.date.year, self.date.month, 1)
            self.name = None

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shiftlist", kwargs={"shiftlist_id": self.pk})

    class Meta:
        verbose_name_plural = "Shiftlijsten"


class Shift(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    shifters = models.ManyToManyField(Lid, blank=True)
    max_shifters = models.PositiveSmallIntegerField()
    extra_info = models.CharField(max_length=500, blank=True, null=True)

    shift_list = models.ForeignKey(Shiftlijst, on_delete=models.CASCADE)
    history = HistoricalRecords(m2m_fields=[shifters])

    def get_start_datetime(self):
        shift = self

        def is_next_day(time_s) -> bool:
            return (
                datetime.time(config.NEXT_DAY_BREAKPOINT, 0, 0)
                > time_s
                > datetime.time(0, 0, 0)
            )

        start = datetime.datetime.combine(
            shift.date + datetime.timedelta(days=1)
            if is_next_day(shift.start)
            else shift.date,
            shift.start,
        )
        return start

    def get_end_datetime(self):
        shift = self

        def is_next_day(time_s) -> bool:
            return (
                datetime.time(config.NEXT_DAY_BREAKPOINT, 0, 0)
                > time_s
                > datetime.time(0, 0, 0)
            )

        end = datetime.datetime.combine(
            shift.date + datetime.timedelta(days=1)
            if is_next_day(shift.end)
            else shift.date,
            shift.end,
        )
        return end

    def __str__(self):
        try:
            return f'{_(formats.date_format(self.date, format="l j F Y"))} | {self.start.isoformat(timespec = "minutes")} - {self.end.isoformat(timespec = "minutes")}'
        except:
            return "ERROR __str__"


class Template(models.Model):
    name = models.CharField(max_length=200)
    template = models.JSONField()

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Onbeschikbaar(models.Model):
    start = models.DateField()
    end = models.DateField()
    info = models.CharField(max_length=500, blank=True, null=True)
    lid = models.ForeignKey(Lid, on_delete=models.CASCADE)


class OnbeschikbaarHerhalend(models.Model):
    start_period = models.DateField()
    end_period = models.DateField()
    weekday = models.PositiveSmallIntegerField()
    start = models.TimeField()
    end = models.TimeField()
    info = models.CharField(max_length=500, blank=True, null=True)
    lid = models.ForeignKey(Lid, on_delete=models.CASCADE)
