from tabnanny import verbose
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
    shift_list = models.ForeignKey(Shiftlijst, on_delete=models.CASCADE)
    def __str__(self):
       return f'{self.date.strftime("%Y %B %d")} | {self.start.isoformat(timespec = "minutes")} - {self.end.isoformat(timespec = "minutes")}'
    
