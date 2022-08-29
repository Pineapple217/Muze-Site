from django.db import models

from leden.models import Lid
from django.utils.translation import gettext as _
from django.utils import formats

class Shiftlijst(models.Model):
    name = models.CharField(max_length = 300, null = True, blank = True)
    date = models.DateField()
    TYPES = [
        ('month', _('month')),
        ('event', _('event'))
    ]
    type = models.CharField(max_length = 100, choices=TYPES)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        if self.type == 'month':
            return _(formats.date_format(self.date , format="F Y"))
        else:
            return self.name
    
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
    def __str__(self):
       return f'{_(formats.date_format(self.date, format="l j F Y"))} | {self.start.isoformat(timespec = "minutes")} - {self.end.isoformat(timespec = "minutes")}'
    
class Template(models.Model):
    name = models.CharField(max_length= 200)
    template = models.JSONField()

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